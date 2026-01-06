# 중이염(Otitis Media) 탐지

이 폴더에는 **중이염 탐지(Otitis Media Detection)** 프로젝트를 재현하고, 탐색하며, 데모까지 실행하는 데 필요한 모든 자료가 포함되어 있습니다.

---

## 💡 프로젝트 개요

- **문제(Problem):** 중이염(급성/만성 중이 감염)은 특히 소아에서 흔하게 발생하며, 신속한 진단이 중요합니다.  
- **데이터(Data):** “Otitis(중이염)” 또는 “Normal(정상)”로 라벨링된 고해상도 이경(otoscopic) 이미지.  
- **접근(Approach):** 이미지 전처리 및 증강(회전, 반전, 밝기/대비 조절)을 수행한 뒤, 128×128 RGB 입력을 사용하는 4개 합성곱 블록 기반 CNN을 학습합니다.  
- **성능(Performance):** 학습 시간이 빠르고 비교적 적은 컴퓨팅 자원으로 **테스트 정확도 75%**를 달성했습니다.  
- **의의(Impact):** 의료진의 진단을 보조하고 원격의료(telemedicine) 시나리오에서 활용 가능한 자동 스크리닝 도구로 확장할 수 있습니다.

---

## 📓 실험 로그(Experiment Log)

세부 실험, 모델 학습, 비교 및 최적 모델 선정 과정은 아래 “Experiment Log” 노트북에 정리되어 있습니다:  
**[Otitis_Media_Experiments.ipynb](./Otitis_Media_Experiments.ipynb)**

---

## 🎯 인터랙티브 데모(Interactive Demo)

브라우저에서 바로 최종 모델을 실행해 볼 수 있습니다.  
귀 이미지를 업로드하면 “Otitis” vs. “Normal” 결과를 실시간으로 확인할 수 있습니다:  
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1waInlrtFBBrWfZmx-O57O9EB3INjh8Hd?usp=sharing)

---

## 📊 발표 자료(Presentation)

프로젝트 개요, 동기, 방법론, 결과를 슬라이드로 정리했습니다:  
**[Google Slides Presentation](https://docs.google.com/presentation/d/1gsz0eFgTKw0zCEPLxbT97Wyz9BMc4WxRIgOsalq3pnc/edit?usp=sharing)**

---

## 📂 폴더 구조(File Structure)

```text
otitis-detection/
├── Otitis_Inference_Interactive_TFLite.ipynb
├── models/
│    └── otitis_cnn_best.tflite
└── requirements.txt

