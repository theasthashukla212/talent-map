# modules/recommendation.py

def recommend_domain(data):

    scores = {
        "Engineering": 0,
        "Medical": 0,
        "Business": 0,
        "Design": 0,
        "Arts & Humanities": 0
    }

    # -------- SUBJECTS --------
    if "PCM" in data["subjects"]:
        scores["Engineering"] += 3

    if "PCB" in data["subjects"]:
        scores["Medical"] += 3

    if "Commerce" in data["subjects"]:
        scores["Business"] += 3

    if "Arts" in data["subjects"]:
        scores["Arts & Humanities"] += 3

    # -------- INTERESTS --------
    if "Technology" in data["interests"]:
        scores["Engineering"] += 2

    if "Biology" in data["interests"]:
        scores["Medical"] += 2

    if "Business" in data["interests"]:
        scores["Business"] += 2

    if "Creativity" in data["interests"]:
        scores["Design"] += 2

    if "Social Work" in data["interests"]:
        scores["Arts & Humanities"] += 2

    # -------- SKILLS --------
    if "Logical Thinking" in data["skills"]:
        scores["Engineering"] += 2

    if "Communication" in data["skills"]:
        scores["Business"] += 2

    if "Creativity" in data["skills"]:
        scores["Design"] += 2

    if "Problem Solving" in data["skills"]:
        scores["Engineering"] += 2

    # -------- BEST DOMAIN --------
    best_domain = max(scores, key=scores.get)

    return best_domain, scores