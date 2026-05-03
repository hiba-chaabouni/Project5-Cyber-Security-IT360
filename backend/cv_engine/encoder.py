import cv2
import numpy as np

def encode_face(gray_face):
    if gray_face is None or gray_face.size == 0:
        return None

    resized = cv2.resize(gray_face, (100, 100))

    lbph = cv2.face.LBPHFaceRecognizer_create(
        radius=1, neighbors=8, grid_x=8, grid_y=8
    )

    lbph.train([resized], np.array([0]))

    histograms = lbph.getHistograms()
    vector = histograms[0].flatten()

    return vector.astype(np.float32)