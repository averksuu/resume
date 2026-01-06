# Notebooks (Pipeline Steps)

이 폴더에는 “Paper is all you need” 파이프라인을 구성하는 노트북이 단계별로 정리되어 있습니다.  
실행 순서는 아래와 같습니다.

## 실행 순서
1. `pdf2md.ipynb`  
2. `md2kor.ipynb`  
3. `md2tex.ipynb`

---

## 01_pdf2md.ipynb — PDF → Markdown (+ figures)
**목적:** 논문 PDF를 구조화된 Markdown으로 변환하고, 이미지/그림을 추출합니다.  
**입력:** `examples/paper3.pdf` (또는 원하는 PDF 경로)  
**출력:**
- `outputs/output.md` (병합된 Markdown)


---

## 02_md2kor.ipynb — Markdown → Korean Markdown
**목적:** Markdown을 섹션 단위로 한국어로 번역합니다.  
**특징:**
- **Title + Abstract**는 함께 번역
- 이후 섹션은 분리하여 번역
**입력:** `outputs/output.md`  
**출력(예시):**
- `outputs/output_ko.md` (병합된 한국어 Markdown)

> ⚠️ 번역 단계는 API 키(예: `OPENAI_API_KEY`)가 필요할 수 있습니다.  
> 키는 코드에 하드코딩하지 말고 환경변수로 설정하세요.

---

## 03_md2tex.ipynb — Korean Markdown → LaTeX
**목적:** 한국어 Markdown을 LaTeX로 변환하여 최종 PDF 컴파일이 가능하도록 합니다.  
**입력:** `outputs/output_ko.md` (또는 병합된 한국어 Markdown)  
**출력:**
- `outputs/paper_ko.tex`

---

## Notes
