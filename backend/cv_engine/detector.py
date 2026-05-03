import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detect_face(frame):
    """
    Takes a BGR numpy array.
    Returns (face_color, face_gray) tuple, or (None, None) if no face found.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    if len(faces) == 0:
        return None, None

    x, y, w, h = faces[0]

    margin = 20
    x = max(0, x - margin)
    y = max(0, y - margin)
    w = min(frame.shape[1] - x, w + 2 * margin)
    h = min(frame.shape[0] - y, h + 2 * margin)

    face_color = frame[y:y+h, x:x+w]
    face_gray  = gray[y:y+h, x:x+w]

    return face_color, face_gray