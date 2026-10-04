# CLI: python check.py <folder of document images>
import glob, os, sys
from checks import ocr, extract, find_issues

folder = sys.argv[1] if len(sys.argv) > 1 else "samples/case_issues"
docs = {}
for path in sorted(glob.glob(os.path.join(folder, "*.png")) + glob.glob(os.path.join(folder, "*.jpg"))):
    f = extract(ocr(path))
    docs[f.get("doc_type") or "unknown"] = f
    print(f"[read] {os.path.basename(path)} -> {f}")

issues = find_issues(docs)
print("\n=== NEEDS ATTENTION ===" if issues else "\n=== No flags (not a legal clearance) ===")
for sev, msg in issues:
    print(f"- [{sev}] {msg}")
print("\nNot legal advice. Have a lawyer verify title.")
