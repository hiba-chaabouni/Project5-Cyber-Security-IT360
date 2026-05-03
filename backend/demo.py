import cv2
import numpy as np
from cv_engine import detect_face, encode_face, match_face

enrolled_faces = []
enroll_counter = 1

def draw_status(frame, message, color=(255, 255, 255)):
    cv2.putText(frame, message, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2, cv2.LINE_AA)

def main():
    global enroll_counter
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("ERROR: Cannot access webcam.")
        return
    import time
    time.sleep(2)

    print("=== Face Auth Demo ===")
    print("Press E to enroll | A to authenticate | Q to quit")
    print("Faces are auto-named: Person1, Person2, etc.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display = frame.copy()
        face_color, face_gray = detect_face(frame)

        if face_gray is not None:
            draw_status(display, "Face detected", color=(0, 255, 0))
        else:
            draw_status(display, "No face detected", color=(0, 0, 255))

        cv2.putText(display, f"Enrolled: {len(enrolled_faces)} face(s)",
                    (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (200, 200, 200), 1, cv2.LINE_AA)

        cv2.imshow("Face Auth — E=Enroll  A=Auth  Q=Quit", display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('e'):
            print("\n[ENROLL] Capturing...")
            _, face_gray = detect_face(frame)
            if face_gray is None:
                print("[ENROLL] FAILED — no face found. Look at the camera.")
            else:
                vector = encode_face(face_gray)
                username = f"Person{enroll_counter}"
                enroll_counter += 1
                enrolled_faces.append({"username": username, "vector": vector})
                print(f"[ENROLL] SUCCESS — '{username}' enrolled.")

        elif key == ord('a'):
            print("\n[AUTH] Authenticating...")
            if not enrolled_faces:
                print("[AUTH] No faces enrolled yet. Press E first.")
            else:
                _, face_gray = detect_face(frame)
                if face_gray is None:
                    print("[AUTH] FAILED — no face found.")
                else:
                    vector = encode_face(face_gray)
                    result = match_face(vector, enrolled_faces)
                    if result["match"]:
                        print(f"[AUTH] ACCESS GRANTED — {result['username']} (score: {result['score']})")
                    else:
                        print(f"[AUTH] ACCESS DENIED (score: {result['score']})")

        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()