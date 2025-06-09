from flask import Flask, request, jsonify
from flask_cors import CORS
from textsum_module import (
    split_sentences,
    determine_top_n,
    summarize,
    image_to_text,
    pdf_to_text
)
import sys
from pathlib import Path

# Flask 앱 초기화
app = Flask(__name__)
CORS(app)  # 프론트엔드 fetch 요청을 허용

# wiki 폴더 경로 추가
sys.path.append(str(Path(__file__).resolve().parent.parent / "wiki"))

# 위키 검색 모듈 import
from wiki_search_module import get_definition

# ===========================
# 텍스트 요약 API
# ===========================
@app.route("/api/summarize", methods=["POST"])
def summarize_text_api():
    data = request.get_json()
    text = data.get("text", "")
    mode = data.get("mode", "")

    if not text.strip():
        return jsonify({"error": "텍스트가 비어 있습니다."}), 400

    try:
        sentences = split_sentences(text)
        top_n = determine_top_n(sentences, mode)
        summary = summarize(text, top_n)
        return jsonify({"summary": " ".join(summary)})
    except Exception as e:
        return jsonify({"error": f"요약 중 오류 발생: {str(e)}"}), 500

# ===========================
# 이미지 요약 API (OCR)
# ===========================
@app.route("/api/summarize/image", methods=["POST"])
def summarize_image_api():
    file = request.files.get("file")
    mode = request.form.get("mode", "")

    if not file:
        return jsonify({"error": "이미지 파일이 없습니다."}), 400

    temp_path = f"temp_{file.filename}"
    file.save(temp_path)

    try:
        text = image_to_text(temp_path)
        if not text.strip():
            return jsonify({"error": "이미지에서 텍스트를 추출하지 못했습니다."}), 400

        sentences = split_sentences(text)
        top_n = determine_top_n(sentences, mode)
        summary = summarize(text, top_n)

        return jsonify({"summary": " ".join(summary)})
    except Exception as e:
        return jsonify({"error": f"OCR 요약 중 오류 발생: {str(e)}"}), 500

# ===========================
# PDF 요약 API
# ===========================
@app.route("/api/summarize/pdf", methods=["POST"])
def summarize_pdf():
    file = request.files.get("file")
    mode = request.form.get("mode", "")

    if not file:
        return jsonify({"error": "PDF 파일이 없습니다."}), 400

    temp_path = f"temp_{file.filename}"
    file.save(temp_path)

    try:
        text = pdf_to_text(temp_path)
        if not text.strip():
            return jsonify({"error": "PDF에서 텍스트를 추출하지 못했습니다."}), 400

        sentences = split_sentences(text)
        top_n = determine_top_n(sentences, mode)
        summary = summarize(text, top_n)

        return jsonify({"summary": " ".join(summary)})
    except Exception as e:
        return jsonify({"error": f"PDF 요약 중 오류 발생: {str(e)}"}), 500

# ===========================
# 위키백과 검색 API
# ===========================
@app.route("/api/wiki", methods=["GET"])
def search_wiki():
    term = request.args.get("term")
    if not term:
        return jsonify({"error": "검색어(term)가 필요합니다."}), 400

    try:
        result = get_definition(term)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"위키 검색 오류: {str(e)}"}), 500

# ===========================
# 실행
# ===========================
if __name__ == "__main__":
    app.run(debug=True, port=5001)
