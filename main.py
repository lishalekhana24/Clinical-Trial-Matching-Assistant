

import json

from data import trials, patients, questions
from llm import ask_llm, check_condition
from matching import check_eligibility, search_trials
from agent import run_agent


print("\n==========================================")
print("     CLINICAL TRIAL MATCHING ASSISTANT")
print("==========================================")

print("\n1. Ask what a clinical trial is")
print("2. Compare zero-shot and few-shot")
print("3. Check eligibility")
print("4. Search trials")
print("5. Run all six assessment questions")
print("6. Select one assessment question")
print("7. Ask any custom question")
print("8. Exit")

choice = input("\nEnter your choice (1-8): ")


# Print the agent answer neatly.
def display_result(result):

    if isinstance(result, dict):
        print("\nSelected Tool:", result["tool_used"])
        print("\nAgent Answer:")
        print(result["answer"])
    else:
        print("\nAgent Answer:")
        print(result)


# OPTION 1
if choice == "1":

    print("\nAssistant:")
    answer = ask_llm("What is a clinical trial? Explain simply.")
    print(answer)


# OPTION 2: Zero-shot and few-shot comparison
elif choice == "2":

    examples = [
        ["I have asthma", "has asthma", "Met"],
        ["I have high blood pressure", "has high blood pressure", "Met"],
        ["I do not have diabetes", "has diabetes", "Not met"],
        ["I do not work nights", "works night shifts", "Not met"],
        ["I did not share diagnosis", "has asthma", "Unknown"],
        ["My medical history is missing", "had recent heart surgery", "Unknown"],
        ["I have migraine", "has migraine", "Met"],
        ["I do not have kidney disease", "has severe kidney disease", "Not met"],
        ["I can attend monthly visits", "can attend monthly visits", "Met"],
        ["I did not say if pregnant", "pregnant", "Unknown"]
    ]

    zero_correct = 0
    few_correct = 0

    print("\nZERO-SHOT AND FEW-SHOT COMPARISON")

    for item in examples:

        zero = check_condition(item[0], item[1], False)
        few = check_condition(item[0], item[1], True)

        if zero.get("result") == item[2]:
            zero_correct += 1

        if few.get("result") == item[2]:
            few_correct += 1

        print("\nCondition:", item[1])
        print("Expected:", item[2])
        print("Zero-shot:", zero.get("result"))
        print("Few-shot:", few.get("result"))

    print("\n========== FINAL COMPARISON ==========")
    print("Zero-shot:", zero_correct, "out of 10")
    print("Few-shot:", few_correct, "out of 10")


# OPTION 3
elif choice == "3":

    patient_id = input("\nEnter patient ID (P001): ")
    trial_id = input("Enter trial ID (T01): ")

    result = check_eligibility(patient_id, trial_id)

    print("\nEligibility result:")
    print(json.dumps(result, indent=4))


# OPTION 4
elif choice == "4":

    condition = input("\nEnter a condition (example diabetes): ")

    result = search_trials(condition=condition)

    print("\nMatching trials:")
    print(json.dumps(result, indent=4))


# OPTION 5: Run all six questions
elif choice == "5":

    test_results = []

    expected_tools = [
        "search_trials",
        "check_eligibility",
        "check_eligibility",
        "search_trials",
        "check_eligibility",
        "none"
    ]

    for i, question in enumerate(questions):

        print("\n==========================================")
        print("Question:", question)

        try:

            result = run_agent(question)

            display_result(result)

            if isinstance(result, dict):
                tool_used = result["tool_used"]
                answer = result["answer"]
            else:
                tool_used = "unknown"
                answer = str(result)

            # Compare the selected tool with the expected tool.
            correct = tool_used == expected_tools[i]

            test_results.append({
                "question": question,
                "tool_used": tool_used,
                "answer": answer,
                "correct_tool": correct
            })

            print("\nCorrect tool:", correct)

        except Exception as error:

            print("\nError:", error)

            test_results.append({
                "question": question,
                "tool_used": "error",
                "answer": str(error),
                "correct_tool": False
            })

    with open("test_results.json", "w") as file:
        json.dump(test_results, file, indent=4)

    print("\n==========================================")
    print("ALL SIX QUESTIONS COMPLETED")
    print("Results saved in test_results.json")
    print("==========================================")


# OPTION 6
elif choice == "6":

    print("\nSELECT AN ASSESSMENT QUESTION")

    for i in range(len(questions)):
        print(str(i + 1) + ". " + questions[i])

    number = input("\nEnter question number (1-6): ")

    if number.isdigit():

        number = int(number)

        if 1 <= number <= len(questions):

            question = questions[number - 1]

            print("\nQuestion:", question)

            result = run_agent(question)
            display_result(result)

        else:
            print("Please enter a number between 1 and 6.")

    else:
        print("Please enter a valid number.")


# OPTION 7
elif choice == "7":

    question = input("\nType your question: ")

    if question.strip() != "":

        result = run_agent(question)
        display_result(result)

    else:
        print("Please enter a question.")


# OPTION 8
elif choice == "8":

    print("\nThank you for using Clinical Trial Matching Assistant!")


else:

    print("\nInvalid choice. Please select 1 to 8.")
