# Project5-Cyber-Security-IT360:

# Web-Based Facial Authentication System

A biometric authentication system that uses real-time facial recognition 
to verify user identity — no passwords required.

Built with OpenCV and Python as part of a security engineering project.

## Overview

This system captures a user's face via webcam, extracts a unique faceprint,
and matches it against enrolled records to grant or deny access.
It prioritizes simplicity, real-time performance, and ease of deployment
over peak accuracy.

## How It Works
| Step | Description |
|------|-------------|
| **Capture** | Camera permission, frame extraction, preprocessing |
| **Detect** | Haar Cascade / DNN crops the face region |
| **Landmark** | 68–478 key facial points mapped |
| **Encode** | LBPH histogram → compact feature vector |
| **Match** | Cosine similarity vs. enrolled faceprints in DB |
| **Decide** | Threshold check → access granted or denied |

---

## Tech Stack

- **Language:** Python 3.x
- **Core Library:** OpenCV (face detection + LBPH recognition)
- **Face Detection:** Haar Cascades / DNN module
- **Feature Encoding:** LBPH (Local Binary Pattern Histograms)

---

## Performance

| Metric | Value |
|--------|-------|
| Feature Vectors | ~50–100 (LBPH histogram-based) |
| Accuracy | ~85–95% (varies with lighting & dataset) |
| Inference Time | ~10–20ms (CPU-friendly, real-time) |

---

## Getting Started

### Prerequisites
```bash
pip install opencv-python numpy
```

### Run
```bash
# Enroll a new user
python enroll.py --name "John"

# Authenticate
python authenticate.py
```

---

## State of the Art — Comparison

| Solution | Accuracy | Web-Ready | Complexity |
|----------|----------|-----------|------------|
| **OpenCV + dlib** | 99.38% | Server-side | Low |
| Face-API.js | ~99.2% | Browser-native | Low |
| DeepFace | 99.6%+ | Server-side | Medium |
| InsightFace | 99.83% | Server-side | High |
| AWS Rekognition | 99.7%+ | Cloud API | Medium |

> This project uses OpenCV for its simplicity and accessibility,
> making it ideal as a first functional implementation.

---

## Limitations

- Accuracy depends on lighting conditions and dataset quality
- No liveness detection implemented (spoofing not fully addressed)
- Not intended for production-grade security systems

---

## Report

Full project report available in `/Security,P5.pdf`

---

## Authors

- **Hiba Chaabouni** - **Ghada Ben Amira**
- **Ali Ayari** — **Aya Yahia**

## Academic Context

> Project 5 — Web-Based Facial Authentication System  
> Security Course — [University of Tunis / Tunis Business School] — 2026
