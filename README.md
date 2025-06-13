# 📝 OCR to JSON Parser

A simple and powerful tool that lets users upload **images or PDFs**, extract readable text using **OCR (Tesseract)**, and return the output in a **clean, structured JSON format**.

Built using **Python**, **Streamlit**, and **PyTesseract**.

---

## 🔍 Features

- 📤 Upload support for **JPG, PNG, and PDF**
- 🧠 Automatic **language detection** using `langdetect`
- 🌐 Supports English, French, and German OCR (Tesseract language packs)
- 🧹 Basic text cleaning (removes extra spaces and line breaks)
- 🔢 Fixes common OCR errors in numbered lists (e.g., `1 Bonjour` → `1. Bonjour`)
- 🔑 Extracts key values like:
  - Invoice number
  - Date
  - Total amount
  - Email
  - Phone number
- 📦 JSON output ready for integration

---# ocr-to-json-parser
