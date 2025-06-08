from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF
from PIL import Image, ImageFilter, ImageOps
import pytesseract
from pdf2image import convert_from_path
import numpy as np

# 형태소 분석기 초기화
okt = Okt()

"""
------입력형태 설정(tesseract ocr 활용)------
"""
# 이미지 전처리(흑백화, 색 반전, 노이즈 제거)
def clean_image(image_path):
    img = Image.open(image_path)
    img = img.convert("L")
    img = ImageOps.invert(img)
    img = img.filter(ImageFilter.MedianFilter())
    return img

# 이미지->텍스트 변환(전처리 포함)
def image_to_text(image_path, preprocess=True):
    if preprocess:
        img = clean_image(image_path)
    else:
        img = Image.open(image_path)
    return pytesseract.image_to_string(img, lang='kor', config='--psm 3')

# pdf->텍스트 변환(각 페이지를 이미지로 변환 후 텍스트 변환)
def pdf_to_text(pdf_path):
    pages = convert_from_path(pdf_path)
    full_text = ""
    for page in pages:
        img = page.convert("L")
        img = ImageOps.invert(img)
        img = img.filter(ImageFilter.MedianFilter())
        text = pytesseract.image_to_string(img, lang='kor', config='--psm 3')
        full_text += text + "\n"
    return full_text

"""
------텍스트 요약 기능------
"""
# 형태소 분석(명사 분리 후 반환)
def tokenize(sent):
    return " ".join(okt.nouns(sent))

# 요약 처리
def summarize(text, top_n=3):
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 5]
    if len(sentences) <= top_n:
        return sentences
    tokenized = [tokenize(s) for s in sentences]
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(tokenized)
    sim_matrix = cosine_similarity(tfidf, tfidf)
    scores = sim_matrix.sum(axis=1)
    ranked_sentences = [sentences[i] for i in np.argsort(scores)[::-1]]
    return ranked_sentences[:top_n]

# 요약 길이 기존 설정
def estimate_top_n(sentences):
    n = len(sentences)
    if n <= 3:      # 3문장 이내->요약 x
        return n
    elif n <= 6:    # 6문장 이하->1문장
        return 1
    elif n <= 10:   # 10문장 이하->3문장
        return 3
    else:
        return max(3, int(n * 0.3))     # 10문장 초과->원래 길이의 30%

# 요약 길이 직접 설정
# mode: "1문장", "3문장", "30%" 중 하나를 선택 / 선택하지 않으면 기존에 설정된 요약 길이로 반환
def determine_top_n(sentences, mode=None):
    n = len(sentences)

    # 사용자 선택에 따라 요약 길이 설정
    if mode == "1문장":
        return 1
    elif mode == "3문장":
        return 3
    elif mode == "30%":
        return max(1, int(n * 0.3))
    else:
        return estimate_top_n(sentences)    # 선택하지 않으면 기존에 설정된 요약 길이로 반환

# 문장 분리 & 문장 리스트 반환
# 마침표 기준으로 분리, 5글자 이하 문장은 제외(반환x)
def split_sentences(text):
    return [s.strip() for s in text.split(".") if len(s.strip()) > 5]

"""
------요약결과 저장------
"""
# 요약 결과 저장(텍스트 파일)
def save_as_text(summary, filename="summary.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for i, s in enumerate(summary, 1):
            f.write(f"{i}. {s}\n")
    print(f"저장 완료: {filename}")

# 요약 결과 저장(pdf 파일)
def save_as_pdf(summary, filename="summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for i, s in enumerate(summary, 1):
        pdf.cell(200, 10, txt=f"{i}. {s}", ln=True)
    pdf.output(filename)
    print(f"저장 완료: {filename}")