# Generates FAKE sample documents (names/numbers invented) for demo + testing.
# Layouts are UNCONFIRMED approximations of Karnataka documents.
import os
from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/arial.ttf"
BOLD = "C:/Windows/Fonts/arialbd.ttf"

CASES = {
    "case_clean": dict(
        owner="Ramesh Kumar S", seller="Venkatesh Rao M", survey="45/2", khata="1123/45",
        area="1200", sale_date="12-03-2021", tax_owner="Ramesh Kumar S", tax_survey="45/2",
        tax_khata="1123/45", tax_paid_upto="2025-26", ec_owner="Ramesh Kumar S",
        ec_survey="45/2", ec_encumbrance="NIL"),
    "case_issues": dict(
        owner="Ramesh Kumar S", seller="Venkatesh Rao M", survey="45/2", khata="1123/45",
        area="1200", sale_date="12-03-2021", tax_owner="Ramesh Kumar", tax_survey="45/3",
        tax_khata="1123/45", tax_paid_upto="2022-23", ec_owner="Venkatesh Rao M",
        ec_survey="45/2", ec_encumbrance="Mortgage to ABC Co-op Bank, Rs 8,00,000, 2019, not released"),
}


def render(path, title, lines):
    img = Image.new("RGB", (900, 700), "white")
    d = ImageDraw.Draw(img)
    d.text((60, 40), title, font=ImageFont.truetype(BOLD, 30), fill="black")
    d.line((60, 90, 840, 90), fill="black", width=2)
    f = ImageFont.truetype(FONT, 24)
    y = 120
    for line in lines:
        d.text((60, y), line, font=f, fill="black")
        y += 48
    img.save(path)


for name, c in CASES.items():
    out = os.path.join("samples", name)
    os.makedirs(out, exist_ok=True)
    render(f"{out}/sale_deed.png", "SALE DEED", [
        f"Seller: {c['seller']}", f"Buyer: {c['owner']}", f"Survey No: {c['survey']}",
        f"Khata No: {c['khata']}", f"Extent: {c['area']} sq ft", f"Date of Registration: {c['sale_date']}"])
    render(f"{out}/encumbrance_certificate.png", "ENCUMBRANCE CERTIFICATE", [
        f"Property Owner: {c['ec_owner']}", f"Survey No: {c['ec_survey']}",
        "Period: 01-04-2011 to 31-03-2024", f"Encumbrances: {c['ec_encumbrance']}"])
    render(f"{out}/tax_receipt.png", "PROPERTY TAX PAID RECEIPT", [
        f"Assessee: {c['tax_owner']}", f"Survey No: {c['tax_survey']}",
        f"Khata No: {c['tax_khata']}", f"Tax paid up to: {c['tax_paid_upto']}"])
print("samples written")
