# FAKE Kannada-labelled docs rendered via headless Edge (Pillow can't shape Kannada here).
# Kannada wording is MY BEST EFFORT and unverified - a Kannada speaker must review it.
import os, subprocess

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE):
    EDGE = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

DOCS = {
    "sale_deed": ("ಕ್ರಯ ಪತ್ರ (SALE DEED)", [
        "ಮಾರಾಟಗಾರರು: Venkatesh Rao M", "ಖರೀದಿದಾರರು: Ramesh Kumar S", "ಸರ್ವೆ ನಂ: 45/2",
        "ಖಾತಾ ನಂ: 1123/45", "ವಿಸ್ತೀರ್ಣ: 1200 ಚ.ಅ", "ನೋಂದಣಿ ದಿನಾಂಕ: 12-03-2021"]),
    "encumbrance_certificate": ("ಋಣಭಾರ ಪ್ರಮಾಣ ಪತ್ರ (ENCUMBRANCE CERTIFICATE)", [
        "ಆಸ್ತಿ ಮಾಲೀಕರು: Ramesh Kumar S", "ಸರ್ವೆ ನಂ: 45/2", "ಅವಧಿ: 01-04-2011 ರಿಂದ 31-03-2024",
        "ಋಣಭಾರ: ಇಲ್ಲ (NIL)"]),
    "tax_receipt": ("ಆಸ್ತಿ ತೆರಿಗೆ ರಸೀದಿ (PROPERTY TAX RECEIPT)", [
        "ತೆರಿಗೆದಾರರು: Ramesh Kumar S", "ಸರ್ವೆ ನಂ: 45/2", "ಖಾತಾ ನಂ: 1123/45",
        "ತೆರಿಗೆ ಪಾವತಿ: 2025-26 ರವರೆಗೆ"]),
}

out = os.path.abspath("samples/case_kannada")
os.makedirs(out, exist_ok=True)
for name, (title, lines) in DOCS.items():
    html = (f"<html><meta charset='utf-8'><body style='font-family:Nirmala UI;font-size:26px;margin:50px;background:white'>"
            f"<h1>{title}</h1><hr>" + "".join(f"<p>{l}</p>" for l in lines) + "</body></html>")
    h = os.path.join(out, f"{name}.html")
    open(h, "w", encoding="utf-8").write(html)
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--window-size=900,700",
                    f"--screenshot={os.path.join(out, name)}.png", "file:///" + h.replace("\\", "/")],
                   capture_output=True, timeout=60)
    os.remove(h)
print("kannada samples:", os.listdir(out))
