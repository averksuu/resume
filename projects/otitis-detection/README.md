# Otitis Media Detection — Interactive Demo (TFLite)

This interactive demo uses a quantized TFLite model (~5 MB) for Otitis Media Detection.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Open `Otitis_Inference_Interactive_TFLite.ipynb` in Jupyter or Colab.  
3. Run all cells and upload your ear image via the widget to see prediction.

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
