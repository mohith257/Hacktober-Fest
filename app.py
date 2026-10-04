# Run: streamlit run app.py   (everything stays on this machine)
import os, tempfile
import streamlit as st
from checks import ocr, extract, find_issues, CFG

st.set_page_config(page_title="Plot Check", page_icon="📄")
st.title("Plot Check")
st.caption("Karnataka plot documents: cross-check, flag gaps. Runs locally; nothing is uploaded anywhere. "
           "Not legal advice.")
st.warning("Rules are unconfirmed - a Karnataka property professional should review them.", icon="⚠️")

files = st.file_uploader("Upload sale deed, EC, tax receipt (and khata if you have it)",
                         type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if files and st.button("Check documents", type="primary"):
    docs = {}
    for f in files:
        with st.spinner(f"Reading {f.name}..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(f.name)[1]) as t:
                t.write(f.getvalue())
            fields = extract(ocr(t.name))
            os.remove(t.name)
        docs[fields.get("doc_type") or "unknown"] = fields
    issues = find_issues(docs)

    st.subheader("Needs attention" if issues else "No flags")
    icon = {"high": "🔴", "medium": "🟠", "low": "🟡"}
    for sev, msg in sorted(issues, key=lambda i: ["high", "medium", "low"].index(i[0])):
        st.write(f"{icon[sev]} {msg}")
    if not issues:
        st.success("Nothing flagged. This is not a legal clearance - have a lawyer verify the title.")

    with st.expander("What was read from each document"):
        for d, fields in docs.items():
            st.markdown(f"**{d.replace('_', ' ')}**")
            st.json({k: v for k, v in fields.items() if v})
