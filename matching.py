
from data import patients, trials
from llm import check_condition


def check_eligibility(patient_id, trial_id):

    patient = None
    trial = None

    for item in patients:
        if item["id"] == patient_id:
            patient = item

    for item in trials:
        if item["id"] == trial_id:
            trial = item

    if patient is None or trial is None:
        return {"status": "Patient or trial not found"}

    checks = []

    # Check age using Python.
    if trial["min_age"] <= patient["age"] <= trial["max_age"]:
        checks.append({
            "criterion": "Age requirement",
            "result": "Met",
            "reason": "Patient age is within the trial age range."
        })
    else:
        checks.append({
            "criterion": "Age requirement",
            "result": "Not met",
            "reason": "Patient age is outside the trial age range."
        })

    # Check inclusion conditions.
    for condition in trial["include"]:

        result = check_condition(
            patient["note"], condition, True
        )

        checks.append({
            "criterion": condition,
            "result": result["result"],
            "reason": result["reason"]
        })

    # Check exclusion conditions.
    for condition in trial["exclude"]:

        result = check_condition(
            patient["note"], condition, True
        )

        if result["result"] == "Met":
            final_result = "Not met"

        elif result["result"] == "Not met":
            final_result = "Met"

        else:
            final_result = "Unknown"

        checks.append({
            "criterion": condition,
            "result": final_result,
            "reason": result["reason"]
        })

    results = []

    for item in checks:
        results.append(item["result"])

    if "Not met" in results:
        status = "Not eligible based on information provided"

    elif "Unknown" in results:
        status = "Cannot decide. More information needed."

    else:
        status = "Potentially eligible. Clinician must review."

    return {
        "patient": patient_id,
        "trial": trial_id,
        "checks": checks,
        "status": status
    }


# FAISS embedding search.
def search_trials(patient_id=None, condition=None):

    from search import search_trials as embedding_search_trials

    return embedding_search_trials(
        patient_id=patient_id,
        condition=condition
    )


# Keyword search.
def keyword_search(word):

    found = []

    for trial in trials:

        trial_text = (
            trial["title"] + " " + trial["condition"]
        ).lower()

        if word.lower() in trial_text:
            found.append(trial)

    return found
