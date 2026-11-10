
from data import trials, patients
from sentence_transformers import SentenceTransformer
import faiss

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

trial_texts = []

for trial in trials:
    text = (
        trial["title"] + " " +
        trial["condition"] + " " +
        " ".join(trial["include"]) + " " +
        " ".join(trial["exclude"])
    )
    trial_texts.append(text)

trial_vectors = model.encode(trial_texts)
trial_vectors = trial_vectors.astype("float32")

faiss.normalize_L2(trial_vectors)

index = faiss.IndexFlatIP(trial_vectors.shape[1])
index.add(trial_vectors)


def keyword_search(note):
    found = []
    words = note.lower().split()

    for trial in trials:
        text = (
            trial["title"] + " " +
            trial["condition"]
        ).lower()

        for word in words:
            word = word.strip(".,!?")

            if len(word) > 4 and word in text:
                if trial not in found:
                    found.append(trial)

    return found


def embedding_search(note):
    vector = model.encode([note])
    vector = vector.astype("float32")

    faiss.normalize_L2(vector)

    scores, positions = index.search(vector, 3)

    found = []

    for score, position in zip(scores[0], positions[0]):

        if position >= 0 and score >= 0.35:
            found.append(trials[int(position)])

    return found


def search_trials(patient_id=None, condition=None):

    note = condition

    if patient_id is not None:
        note = None

        for patient in patients:
            if patient["id"] == patient_id:
                note = patient["note"]
                break

    if not note:
        return {"error": "Patient or condition not found"}

    found = embedding_search(note)

    answer = []

    for trial in found:
        answer.append({
            "id": trial["id"],
            "title": trial["title"]
        })

    return answer


if __name__ == "__main__":

    print("\nCOMPARING SEARCH METHODS")

    for patient in patients[:4]:

        print("\nPatient:", patient["id"])

        keyword_results = keyword_search(patient["note"])
        embedding_results = embedding_search(patient["note"])

        print("Keyword search:")
        print([trial["id"] for trial in keyword_results])

        print("Embedding search:")
        print([trial["id"] for trial in embedding_results])