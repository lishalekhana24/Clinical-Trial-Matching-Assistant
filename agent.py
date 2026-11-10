
import json

from llm import client, model_name
from matching import search_trials, check_eligibility

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_trials",
            "description": "Find possible clinical trials for a patient or condition.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {"type": "string"},
                    "condition": {"type": "string"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_eligibility",
            "description": "Check patient eligibility for a clinical trial.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {"type": "string"},
                    "trial_id": {"type": "string"}
                },
                "required": ["patient_id", "trial_id"]
            }
        }
    }
]


def run_agent(question):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a Clinical Trial Matching Assistant. "
                "Use only synthetic patient and trial data. "
                "Use search_trials for trial search questions. "
                "Use check_eligibility for eligibility questions. "
                "Search results are possible matches, not confirmed eligibility. "
                "Never guess missing information. "
                "Unknown must remain Unknown. "
                "Never recommend medicines or give medical advice. "
                "Refuse unrelated questions. "
                "Do not claim a trial is recruiting unless the data confirms it. "
                "Use clean Markdown formatting. "
                "Every eligibility answer must end with exactly: "
                "Final decision rests with the clinician."
                "Use only information returned by the Python tools."
                "Never invent trial locations, recruitment status, enrollment numbers,"
                "or other details that are not present in the database."
                "For search questions, display only the trial ID and title returned by the tool."
                "Always call the appropriate Python tool for patient trial searches"
                "and eligibility questions. Do not answer these questions from memory."
            )
        },
        {"role": "user", "content": question}
    ]

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if not message.tool_calls:
        return {
            "tool_used": "none",
            "answer": message.content or
            "I can only help with clinical trial matching."
        }

    messages.append(message)

    used_tools = []
    used_eligibility = False

    for tool_call in message.tool_calls:

        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print("Tool selected:", tool_name)
        used_tools.append(tool_name)

        if tool_name == "search_trials":

            result = search_trials(
                patient_id=arguments.get("patient_id"),
                condition=arguments.get("condition")
            )

        elif tool_name == "check_eligibility":

            used_eligibility = True

            result = check_eligibility(
                arguments.get("patient_id"),
                arguments.get("trial_id")
            )

        else:
            result = {"error": "Unknown tool"}

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

    final_response = client.chat.completions.create(
        model=model_name,
        messages=messages
    )

    answer = final_response.choices[0].message.content or ""

    # Remove unwanted formatting artifacts.
    answer = answer.replace("> **", "").strip()

    disclaimer = "Final decision rests with the clinician."

    if used_eligibility:
        answer = answer.replace(disclaimer, "").strip()
        answer += "\n\n" + disclaimer
    else:
        answer = answer.replace(disclaimer, "").strip()

    return {
        "tool_used": ", ".join(used_tools),
        "answer": answer
    }