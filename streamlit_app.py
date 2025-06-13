import streamlit as st
import os
from ocr_utils import load_image_from_upload, extract_text, clean_text, structure_to_json

st.set_page_config(page_title="OCR to JSON", layout="centered")
st.title("📄 OCR to JSON Parser")

st.markdown("Upload a scanned PDF or image. The app will auto-detect language, extract text, and return structured JSON.")

uploaded_file = st.file_uploader("Upload JPG, PNG, or PDF", type=["jpg", "png", "pdf"])

if uploaded_file:
    file_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("🔍 Performing OCR..."):
        images = load_image_from_upload(file_path)
        full_text = ' '.join([clean_text(extract_text(img)) for img in images])
        result = structure_to_json(full_text)

    st.success("✅ OCR complete!")
    st.subheader("📋 Extracted JSON:")
    st.json(result)

    st.download_button("📥 Download JSON", data=str(result).encode('utf-8'),
                       file_name="ocr_output.json", mime="application/json")
