# Clinical Trial Matching Assistant (VS Code beginner version)

This is a simple Python project using lists, dictionaries, loops, `if` statements and small functions.
All patient and trial records are fictional.

## 1. Open in VS Code

1. Extract this folder.
2. Open VS Code.
3. Select **File → Open Folder** and choose `Clinical_Trial_Matching_VSCode`.
4. Open **Terminal → New Terminal**.

## 2. Create and activate a virtual environment

### Windows PowerShell

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

### Ubuntu / WSL

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install the package

```bash
python -m pip install -r requirements.txt
```

## 4. Run the project

```bash
python main.py
```

When asked, paste your Groq API key into the hidden prompt. The key is not saved in the project.

## 5. Menu

- `1`: Ask Groq what a clinical trial is.
- `2`: Compare zero-shot and few-shot on 10 examples.
- `3`: Check one patient against one trial.
- `4`: Search trials using a condition keyword.
- `5`: Run all six assessment questions and save `test_results.json`.

The project also creates `trials.json`, `patients.json` and `test_questions.md`.


