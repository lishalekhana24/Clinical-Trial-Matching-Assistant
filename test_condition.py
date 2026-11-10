from llm import check_condition
from data import patients

for patient in patients:

    if patient["id"] == "P002":
        print("P002 asthma:")
        print(check_condition(
            patient["note"], "has asthma", True
        ))

    if patient["id"] == "P004":
        print("P004 recent surgery:")
        print(check_condition(
            patient["note"], "recent heart surgery", True
        ))