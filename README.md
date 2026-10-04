# Plot Check

Cross-checks Karnataka plot documents (sale deed, encumbrance certificate, property tax receipt) and flags
what needs a human's attention. It never gives a verdict on a property.

Everything runs locally: Tesseract OCR + Gemma 3 4B via Ollama. No document leaves the machine.

## Run
1. Install Ollama, `ollama pull gemma3:4b`, and Tesseract (with `eng` and `kan` in `tessdata/`).
2. `python -m venv .venv && .venv\Scripts\pip install pillow requests streamlit numpy`
3. `python gen_docs.py` and `python gen_kannada.py` write FAKE sample documents.
4. `streamlit run app.py`, or `python check.py samples/case_issues` for the CLI.

## How it works
- `checks.py`: OCR, Gemma extracts fields as JSON, plain code does every check. The model never decides.
- `config.json`: required documents, key fields (survey no, khata no), tax cut-off year. Edit rules here.

## Known limits (be honest)
- Rules and document layouts are UNCONFIRMED and need review by a Karnataka property professional.
- Tested only on synthetic documents (clean, degraded, and Kannada-labelled). Real scans are untested.
- Gemma 4B put a Kannada tax date in the wrong field; the tool now flags unreadable fields instead of skipping.
- Kannada sample wording is my best effort and unverified.
- No valuation feature: no real comparable-sales data was available.
