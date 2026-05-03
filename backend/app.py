import cv2
import numpy as np
import base64
import jwt
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

from cv_engine import detect_face, encode_face, match_face
from database import init_db, insert_user, insert_faceprint, get_all_faceprints, log_event

app = Flask(__name__)
CORS(app)

SECRET_KEY = "your_secret_key_change_this"

init_db()

def decode_frame(base64_str):
    img_data = base64.b64decode(base64_str)
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return frame

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/enroll", methods=["POST"])
def enroll():
    data = request.get_json()
    username = data.get("username")
    frame_b64 = data.get("frame")

    if not username or not frame_b64:
        return jsonify({"error": "username and frame are required"}), 400

    frame = decode_frame(frame_b64)
    _, face_gray = detect_face(frame)

    if face_gray is None:
        return jsonify({"error": "no face detected in frame"}), 400

    vector = encode_face(face_gray)

    try:
        user_id = insert_user(username)
        insert_faceprint(user_id, vector)
        log_event(username, "enroll", "success", request.remote_addr)
        return jsonify({"status": "enrolled", "user_id": user_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/authenticate", methods=["POST"])
def authenticate():
    data = request.get_json()
    frame_b64 = data.get("frame")

    if not frame_b64:
        return jsonify({"error": "frame is required"}), 400

    frame = decode_frame(frame_b64)
    _, face_gray = detect_face(frame)

    if face_gray is None:
        log_event(None, "authenticate", "no_face", request.remote_addr)
        return jsonify({"match": False, "reason": "no face detected"}), 200

    vector = encode_face(face_gray)
    stored = get_all_faceprints()

    if not stored:
        return jsonify({"match": False, "reason": "no enrolled users"}), 200

    result = match_face(vector, stored)

    if result["match"]:
        token = jwt.encode({
            "username": result["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")

        log_event(result["username"], "authenticate", "granted", request.remote_addr)
        return jsonify({
            "match": True,
            "user": result["username"],
            "score": result["score"],
            "token": token
        })
    else:
        log_event(None, "authenticate", "denied", request.remote_addr)
        return jsonify({"match": False, "score": result["score"]})

@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({"status": "logged_out"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)