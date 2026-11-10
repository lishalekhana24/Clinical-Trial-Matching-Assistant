# Clinical Trial Matching Assistant

## 1. Project Goal

The goal of this project is to build a Clinical Trial Matching Assistant using Generative AI.

The assistant helps identify possible clinical trials for patients based on their age, medical conditions, and other information.

The project uses synthetic patient and clinical trial data stored in JSON files.

## 2. Tools Used by the Agent

The agent uses two Python tools.

### Tool 1: search_trials

**Purpose:** Find possible clinical trials for a patient or medical condition.

**Inputs:**
- `patient_id` – Patient ID.
- `condition` – Medical condition.

**Working:**
- Uses Sentence Transformers to convert trial information into embeddings.
- Uses FAISS to find similar clinical trials.
- Returns possible matching trial IDs and titles.

### Tool 2: check_eligibility

**Purpose:** Check whether a patient meets the requirements of a particular clinical trial.

**Inputs:**
- `patient_id` – Patient ID.
- `trial_id` – Clinical trial ID.

**Working:**
- Checks the patient's age using Python.
- Uses the Groq LLM to evaluate inclusion and exclusion criteria.
- Returns one of three results:
  - Met
  - Not met
  - Unknown
- Provides a reason for each criterion.

## 3. Agent Workflow

1. The user enters a question.
2. The Groq LLM understands the question.
3. The LLM selects the appropriate Python tool.
4. The selected tool executes.
5. The tool result is sent back to the LLM.
6. The LLM generates the final response.
7. The application displays the selected tool and answer.

## 4. Rules and Guardrails

- Use only synthetic patient and clinical trial data.
- Never assume missing patient information.
- Return Unknown when information is unavailable.
- Search results are possible matches, not confirmed eligibility.
- Do not provide medical advice or recommend medicines.
- Refuse unrelated questions.
- Never invent trial details that are not present in the database.
- Every eligibility answer must end with:

  **Final decision rests with the clinician.**

## 5. Technologies Used

- Python
- Groq API
- Large Language Model (LLM)
- Sentence Transformers
- FAISS
- JSON
- VS Code

## 6. Expected Output

The assistant should:
- Search for possible clinical trials.
- Check patient eligibility.
- Explain why criteria are met, not met, or unknown.
- Select the correct tool based on the user's question.
- Generate clear responses while following safety rules.