from flask import Flask, request, jsonify
from utils import extract_text_from_pdf, extract_text_from_docx
from summarizer import generate_summary

app = Flask(__name__)

@app.route("/summarize/", methods=["POST"])
def summarize():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    lang = request.form.get("language", "en")

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        file_bytes = file.read()

        # Extract text based on extension
        if file.filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_bytes)
        elif file.filename.lower().endswith((".doc", ".docx")):
            text = extract_text_from_docx(file_bytes)
        else:
            return jsonify({"error": "Unsupported file format"}), 400

        if not text.strip():
            return jsonify({"error": "No text found in document"}), 400

        summary = generate_summary(text, lang)

        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
