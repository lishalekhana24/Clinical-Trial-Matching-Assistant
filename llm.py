import json
import getpass
from groq import Groq

print("Enter your new Groq API key.")
api_key = getpass.getpass("Groq API key: ").strip()

client = Groq(api_key=api_key)
model_name = "openai/gpt-oss-20b"


def ask_llm(prompt):

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


def check_condition(note, condition, few_shot):

    examples = ""

    if few_shot == True:
        examples = """
        Example 1:
        Patient note: I have asthma.
        Condition: has asthma
        Answer: {"result":"Met","reason":"Patient mentions asthma."}

        Example 2:
        Patient note: I do not have asthma.
        Condition: has asthma
        Answer: {"result":"Not met","reason":"Patient denies asthma."}

        Example 3:
        Patient note: Diagnosis not shared.
        Condition: has asthma
        Answer: {"result":"Unknown","reason":"Asthma information is missing."}

        Example 4:
        Patient note: I have a heart condition.
        Condition: recent heart surgery
        Answer: {"result":"Unknown","reason":"Surgery information is missing."}
        """

    prompt = """
    Check the condition using only the patient note.

    Rules:
    1. Met means the note clearly confirms the condition.
    2. Not met means the note clearly denies the condition.
    3. Unknown means information is missing or unclear.
    4. Never assume an unmentioned condition is false.
    5. Never guess medical information.
    6. Return only valid JSON.
    7. Result must be Met, Not met or Unknown.
    """

    prompt += examples
    prompt += "\nPatient note: " + note
    prompt += "\nCondition: " + condition
    prompt += '\nReturn: {"result":"Met/Not met/Unknown","reason":"one-line reason"}'

    answer = ask_llm(prompt)

    start = answer.find("{")
    end = answer.rfind("}") + 1

    try:
        result = json.loads(answer[start:end])

        if result.get("result") not in ["Met", "Not met", "Unknown"]:
            result = {
                "result": "Unknown",
                "reason": "Invalid AI response"
            }

    except (ValueError, TypeError, AttributeError):
        result = {
            "result": "Unknown",
            "reason": "Could not read AI response"
        }

    return result