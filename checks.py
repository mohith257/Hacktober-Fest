# Shared by check.py (CLI) and app.py (Streamlit). OCR -> Gemma extraction -> plain-code checks.
import json, os, re, subprocess
from difflib import SequenceMatcher
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
ENV = {**os.environ, "TESSDATA_PREFIX": os.path.join(HERE, "tessdata")}
OLLAMA = "http://localhost:11434/api/generate"
FIELDS = ["doc_type", "owner_name", "seller_name", "survey_no", "khata_no", "area_sqft", "date",
          "tax_paid_upto", "encumbrances"]
TYPES = ["sale_deed", "encumbrance_certificate", "tax_receipt", "unknown"]
EXPECTED = {"sale_deed": ["owner_name", "seller_name", "survey_no", "khata_no"],
            "encumbrance_certificate": ["owner_name", "survey_no", "encumbrances"],
            "tax_receipt": ["owner_name", "survey_no", "khata_no", "tax_paid_upto"]}  # UNCONFIRMED


def ocr(path):
    return subprocess.run([TESS, path, "stdout", "-l", CFG["ocr_langs"]], capture_output=True,
                          text=True, encoding="utf-8", env=ENV).stdout


def extract(text):
    prompt = (f"Extract fields from the OCR text of a Karnataka property document. Return JSON with keys {FIELDS}. "
              f"doc_type must be one of {TYPES}. Transliterate Kannada names to English. Translate nothing else. "
              "Use null if absent; copy values exactly, do not guess. owner_name is the owner/buyer/assessee; "
              "seller_name only for sale deeds. Digits in Kannada script -> ASCII digits.\n\n" + text)
    r = requests.post(OLLAMA, json={"model": CFG["model"], "prompt": prompt, "stream": False,
                                    "format": "json", "options": {"temperature": 0}}, timeout=300)
    return json.loads(r.json()["response"])


def norm(v):
    return re.sub(r"[^a-z0-9/]", "", str(v).lower()) if v else None


def similar(a, b):
    return SequenceMatcher(None, norm(a) or "", norm(b) or "").ratio()


def find_issues(docs):
    """docs: {doc_type: fields}. Returns list of (severity, message). Never a legal verdict."""
    out = []
    for d in CFG["required_docs"]:
        if d not in docs:
            out.append(("high", f"Missing document: {d.replace('_', ' ')}"))
    for f in CFG["match_fields"]:
        vals = {d: v[f] for d, v in docs.items() if v.get(f)}
        for a in vals:
            for b in vals:
                if a < b and norm(vals[a]) != norm(vals[b]):
                    s = similar(vals[a], vals[b])
                    if f == "owner_name" and s >= CFG["name_similarity_ok"]:
                        out.append(("low", f"Owner name slightly different ({a}: '{vals[a]}' vs {b}: '{vals[b]}') - likely initials/spelling, confirm"))
                    else:
                        out.append(("high", f"{f.replace('_', ' ')} differs: {a}='{vals[a]}' vs {b}='{vals[b]}'"))
    for d, fields in EXPECTED.items():  # never skip a check silently
        for f in fields:
            if d in docs and not docs[d].get(f):
                out.append(("medium", f"Could not read {f.replace('_', ' ')} from {d.replace('_', ' ')} - check manually"))
    ec = docs.get("encumbrance_certificate", {})
    if ec.get("encumbrances") and norm(ec["encumbrances"]) not in ("nil", "none"):
        out.append(("high", f"Encumbrance listed on EC: {ec['encumbrances']}"))
    paid = (docs.get("tax_receipt", {}).get("tax_paid_upto") or "")[:4]
    if paid.isdigit() and int(paid) < CFG["min_tax_paid_year"]:
        out.append(("medium", f"Property tax paid only up to {docs['tax_receipt']['tax_paid_upto']}"))
    return out
