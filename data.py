import json

# Fictional clinical trial data
trials = [
    {"id": "T01", "title": "Diabetes Study", "condition": "diabetes", "min_age": 30, "max_age": 70, "include": ["has diabetes", "can attend monthly visits"], "exclude": ["pregnant", "severe kidney disease"]},
    {"id": "T02", "title": "Blood Pressure Study", "condition": "high blood pressure", "min_age": 40, "max_age": 75, "include": ["has high blood pressure"], "exclude": ["severe heart failure"]},
    {"id": "T03", "title": "Asthma Study", "condition": "asthma", "min_age": 18, "max_age": 60, "include": ["has asthma"], "exclude": ["severe asthma hospital stay"]},
    {"id": "T04", "title": "Sleep Study", "condition": "sleep problems", "min_age": 21, "max_age": 65, "include": ["has sleep difficulties"], "exclude": ["works night shifts"]},
    {"id": "T05", "title": "Heart Study", "condition": "heart disease", "min_age": 45, "max_age": 80, "include": ["has a heart condition"], "exclude": ["recent heart surgery"]},
    {"id": "T06", "title": "Migraine Study", "condition": "migraine", "min_age": 18, "max_age": 55, "include": ["has migraine"], "exclude": ["cannot describe headache history"]},
    {"id": "T07", "title": "Arthritis Study", "condition": "arthritis", "min_age": 35, "max_age": 75, "include": ["has arthritis"], "exclude": ["recent joint replacement"]},
    {"id": "T08", "title": "Anemia Study", "condition": "anemia", "min_age": 18, "max_age": 65, "include": ["has anemia"], "exclude": ["emergency blood transfusion"]}
]

patients = [
    {"id": "P001", "age": 52, "note": "I have diabetes. I can attend monthly visits. I am not pregnant and have no kidney disease."},
    {"id": "P002", "age": 48, "note": "I have high blood pressure. I do not have severe heart failure."},
    {"id": "P003", "age": 27, "note": "I have asthma."},
    {"id": "P004", "age": 62, "note": "I have sleep difficulties. I do not work night shifts."},
    {"id": "P005", "age": 50, "note": "I have a heart condition. I have not shared details about recent surgery."},
    {"id": "P006", "age": 40, "note": "I have not shared my diagnosis or medical history."}
]

questions = [
    "Which trials could patient P001 join?",
    "Is patient P002 eligible for trial T03?",
    "Why is patient P004 not eligible for trial T05?",
    "Which trials are available for diabetes patients?",
    "Is patient P006 eligible for trial T01?",
    "What medicine should patient P002 take?"
]

# Save the data files when this file is imported or run.
with open("trials.json", "w") as file:
    json.dump(trials, file, indent=4)

with open("patients.json", "w") as file:
    json.dump(patients, file, indent=4)

with open("test_questions.md", "w") as file:
    for number, question in enumerate(questions, start=1):
        file.write(str(number) + ". " + question + "\n")
