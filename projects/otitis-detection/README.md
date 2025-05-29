# Otitis Media Detection

This folder contains everything needed to reproduce, explore and demo the Otitis Media Detection project.

---

## 💡 Project Overview

- **Problem:** Otitis media (acute or chronic middle ear infection) is a common condition, especially in children, requiring timely diagnosis.  
- **Data:** High-resolution otoscopic photographs labeled as “Otitis” or “Normal.”  
- **Approach:** Preprocess and augment images (rotations, flips, brightness/contrast), then train a CNN with four convolutional blocks on 128×128 RGB inputs.  
- **Performance:** Achieved **75%** test accuracy with fast training times and modest computational requirements.  
- **Impact:** Provides an automated screening tool to assist clinicians and support telemedicine applications.


## 📓 Experiment Log

Detailed experiments, model training, comparison and best-model selection are documented in the “Experiment Log” notebook:  
**[Otitis_Media_Experiments.ipynb](./Otitis_Media_Experiments.ipynb)**

---

## 🎯 Interactive Demo

Try the final model right in your browser — upload your own ear image and see “Otitis” vs. “Normal” in real time:  
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1waInlrtFBBrWfZmx-O57O9EB3INjh8Hd?usp=sharing)


---

## 📊 Presentation

Project overview, motivation, methodology and results in slides:  
**[Google Slides Presentation](https://docs.google.com/presentation/d/1gsz0eFgTKw0zCEPLxbT97Wyz9BMc4WxRIgOsalq3pnc/edit?usp=sharing)**

---

## 📂 File Structure



## Project Structure

```
otitis-detection/
├── Otitis_Inference_Interactive_TFLite.ipynb
├── models/
│    └── otitis_cnn_best.tflite
└── requirements.txt
```

## Model Details

- Input: 128×128 RGB image, normalized to [0,1].
- Output: Probability score (>=0.5 → Otitis, else Normal).
