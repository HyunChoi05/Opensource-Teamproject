import os
import numpy as np
import re
from PIL import Image, ImageFilter, ImageOps
from pdf2image import convert_from_path
import pytesseract
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fpdf import FPDF
from multiprocessing import Pool

import cv2
from skimage.transform import rotate
from skimage.color import rgb2gray
from skimage.feature import canny
from skimage.transform import hough_line, hough_line_peaks
from scipy.stats import mode

# OCR 전처리 함수

def deskew_image(pil_image: Image.Image) -> Image.Image:
    try:
        image = np.array(pil_image)
        if len(image.shape) == 3:
            grayscale = rgb2gray(image)
        else:
            grayscale = image
        edges = canny(grayscale, sigma=3.0)
        h, theta, d = hough_line(edges)
        accum, angles, dists = hough_line_peaks(h, theta, d, num_peaks=20)
        if not angles.size:
            return pil_image
        angle_deg = mode(np.rad2deg(angles))[0]
        if np.abs(angle_deg) < 1.0:
            return pil_image
        rotated_image = rotate(image, angle_deg, resize=True, mode='constant', cval=1, preserve_range=True) * 255
        return Image.fromarray(rotated_image.astype(np.uint8))
    except Exception as e:
        print(f"[deskew_image 오류] {e}")
        return pil_image

def preprocess_image_advanced(pil_image: Image.Image) -> Image.Image:
    try:
        gray = np.array(pil_image.convert('L'))
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        return Image.fromarray(thresh)
    except Exception as e:
        print(f"[preprocess_image_advanced 오류] {e}")
        return pil_image

# OCR 실행 함수

def ocr_with_tesseract(pil_image: Image.Image, lang='kor') -> str:
    try:
        config = '--oem 3 --psm 3'
        return pytesseract.image_to_string(pil_image, lang=lang, config=config)
    except Exception as e:
        print(f"[ocr_with_tesseract 오류] {e}")
        return ""

def image_to_text_advanced(image_path):
    try:
        img = Image.open(image_path)
        img = deskew_image(img)
        img = preprocess_image_advanced(img)
        return ocr_with_tesseract(img, lang='kor')
    except Exception as e:
        print(f"[image_to_text_advanced 오류] {e}")
        return ""

# 병렬용 페이지 OCR 함수
def process_pdf_page(page):
    try:
        img = deskew_image(page)
        img = preprocess_image_advanced(img)
        return ocr_with_tesseract(img, lang='kor')
    except Exception as e:
        print(f"[PDF 페이지 처리 오류] {e}")
        return ""

def pdf_to_text_parallel(pdf_path):
    try:
        pages = convert_from_path(pdf_path, dpi=300)
        with Pool() as pool:
            texts = pool.map(process_pdf_page, pages)
        return "\n".join(texts)
    except Exception as e:
        print(f"[pdf_to_text_parallel 오류] {e}")
        return ""

# 텍스트 요약 처리

okt = Okt()

def split_sentences(text):
    return [s.strip() for s in re.split(r'[.!?]\s+', text) if len(s.strip()) > 5]

def tokenize(sent):
    return " ".join(okt.nouns(sent))

def summarize(text, top_n=3):
    sentences = split_sentences(text)
    if len(sentences) <= top_n:
        return sentences
    tokenized = [tokenize(s) for s in sentences]
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(tokenized)
    sim_matrix = cosine_similarity(tfidf, tfidf)
    scores = sim_matrix.sum(axis=1)
    ranked_sentences = [sentences[i] for i in np.argsort(scores)[::-1]]
    return ranked_sentences[:top_n]

def estimate_top_n(sentences):
    n = len(sentences)
    if n <= 3:
        return n
    elif n <= 6:
        return 1
    elif n <= 10:
        return 3
    else:
        return max(3, int(n * 0.3))

def determine_top_n(sentences, mode=None):
    n = len(sentences)
    if mode == "1문장":
        return 1
    elif mode == "3문장":
        return 3
    elif mode == "30%":
        return max(1, int(n * 0.3))
    else:
        return estimate_top_n(sentences)

# 결과 저장 (한글 PDF 대응)

def save_as_text(summary, filename="summary.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for i, s in enumerate(summary, 1):
                f.write(f"{i}. {s}\n")
        print(f"저장 완료: {filename}")
    except Exception as e:
        print(f"[save_as_text 오류] {e}")

def save_as_pdf(summary, filename="summary.pdf"):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('Nanum', '', 'NanumGothic.ttf', uni=True)
        pdf.set_font("Nanum", size=12)
        for i, s in enumerate(summary, 1):
            pdf.multi_cell(0, 10, txt=f"{i}. {s}")
        pdf.output(filename)
        print(f"저장 완료: {filename}")
    except Exception as e:
        print(f"[save_as_pdf 오류] {e}")

# ===========================
# 실행 예시
# ===========================

if __name__ == "__main__":
    file_path = "test.pdf"  # 또는 "test.jpg"
    
    if not os.path.exists(file_path):
        print("파일이 존재하지 않습니다.")
    else:
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == '.pdf':
            text = pdf_to_text_parallel(file_path)
        elif ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            text = image_to_text_advanced(file_path)
        else:
            raise ValueError("지원하지 않는 파일 형식입니다.")
        
        sentences = split_sentences(text)
        top_n = determine_top_n(sentences, mode="30%")
        summary = summarize(text, top_n=top_n)
        save_as_text(summary)
        save_as_pdf(summary)
