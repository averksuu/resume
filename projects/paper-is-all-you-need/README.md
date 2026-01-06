# Paper is all you need — 연구 논문 번역 파이프라인 (PDF → MD → KO → LaTeX)

영어 연구 논문을 **구조(제목/소제목, 리스트, 표, 수식)를 유지한 채** 한국어로 번역하고, 출판 가능한 형태의 한국어 PDF로 출력하는 가벼운 파이프라인입니다.

## What it does
본 프로젝트는 논문 PDF를 구조화된 Markdown으로 변환한 뒤, LLM을 사용해 섹션 단위로 한국어 번역을 수행하고, 번역된 한국어 Markdown을 LaTeX로 변환하여 최종 컴파일(예: Overleaf)까지 이어지도록 구성했습니다.

## Pipeline
1) **PDF → Markdown (+ figures)**
   - PDF 페이지를 파싱하고 그림을 추출한 뒤, 하나로 합쳐진 `output.md`를 생성합니다.

2) **Markdown → Korean Markdown**
   - **Title + Abstract**는 함께 번역하고, 나머지 섹션은 분리하여 번역합니다.
   - 섹션별 결과물 및 병합된 한국어 Markdown을 생성합니다.

3) **Korean Markdown → LaTeX**
   - Markdown에서 섹션 단위 JSON을 추출하고, 단일 `paper.tex`를 생성합니다.

## Repository structure
```text
projects/paper-is-all-you-need/
├── notebooks/                 # 파이프라인 노트북
├── examples/                  # 데모 입력/출력 PDF
└── README.md
