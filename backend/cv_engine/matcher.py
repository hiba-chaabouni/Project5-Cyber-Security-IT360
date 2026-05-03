import numpy as np

THRESHOLD = 0.6

def cosine_similarity(vec_a, vec_b):
    dot = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def match_face(query_vector, stored_entries):
    best_score = -1.0
    best_username = None

    for entry in stored_entries:
        score = cosine_similarity(query_vector, entry["vector"])
        if score > best_score:
            best_score = score
            best_username = entry["username"]

    matched = best_score >= THRESHOLD

    return {
        "match": matched,
        "username": best_username if matched else None,
        "score": round(float(best_score), 4)
    }