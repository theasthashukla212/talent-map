# modules/recommendation.py
# Rule-based domain scoring using the full 8-section questionnaire

def recommend_domain(data):
    """
    Score broad domains based on all sections of the questionnaire.
    Returns (best_domain, scores_dict).
    """

    scores = {
        "Engineering & Technology": 0,
        "Medical & Healthcare": 0,
        "Business & Management": 0,
        "Creative & Design": 0,
        "Arts & Humanities": 0,
        "Science & Research": 0,
        "Education & Social Work": 0,
    }

    # ──────── Section 1: Academic Background ────────
    stream = data.get("stream", "")
    if stream == "PCM":
        scores["Engineering & Technology"] += 3
        scores["Science & Research"] += 2
    elif stream == "PCB":
        scores["Medical & Healthcare"] += 3
        scores["Science & Research"] += 2
    elif stream == "Commerce":
        scores["Business & Management"] += 3
    elif stream == "Arts":
        scores["Arts & Humanities"] += 3
        scores["Creative & Design"] += 1

    for subj in data.get("fav_subjects", []):
        if subj == "Mathematics":
            scores["Engineering & Technology"] += 1
            scores["Science & Research"] += 1
        elif subj == "Biology":
            scores["Medical & Healthcare"] += 2
        elif subj == "Computer Science":
            scores["Engineering & Technology"] += 2
        elif subj == "Economics":
            scores["Business & Management"] += 2
        elif subj == "Psychology":
            scores["Education & Social Work"] += 1
            scores["Medical & Healthcare"] += 1
        elif subj == "Business Studies":
            scores["Business & Management"] += 2

    strength = data.get("academic_strength", "")
    if strength == "Problem Solving":
        scores["Engineering & Technology"] += 1
    elif strength == "Practical":
        scores["Engineering & Technology"] += 1
        scores["Medical & Healthcare"] += 1
    elif strength == "Theory":
        scores["Science & Research"] += 1

    # ──────── Section 2: Interest Area ────────
    for act in data.get("activities", []):
        if act == "Coding":
            scores["Engineering & Technology"] += 2
        elif act == "Drawing / Designing":
            scores["Creative & Design"] += 2
        elif act == "Teaching":
            scores["Education & Social Work"] += 2
        elif act == "Helping People":
            scores["Education & Social Work"] += 1
            scores["Medical & Healthcare"] += 1
        elif act == "Business":
            scores["Business & Management"] += 2
        elif act == "Research":
            scores["Science & Research"] += 2
        elif act == "Writing":
            scores["Arts & Humanities"] += 2
        elif act == "Public Speaking":
            scores["Business & Management"] += 1

    work_type = data.get("work_type", "")
    if work_type == "Technical":
        scores["Engineering & Technology"] += 2
    elif work_type == "Creative":
        scores["Creative & Design"] += 2
    elif work_type == "Analytical":
        scores["Science & Research"] += 2
    elif work_type == "Social":
        scores["Education & Social Work"] += 2
    elif work_type == "Management":
        scores["Business & Management"] += 2

    work_env = data.get("work_env", "")
    if work_env == "Lab Work":
        scores["Science & Research"] += 1
        scores["Medical & Healthcare"] += 1
    elif work_env == "Startup":
        scores["Engineering & Technology"] += 1
        scores["Business & Management"] += 1
    elif work_env == "Remote Work":
        scores["Engineering & Technology"] += 1

    # ──────── Section 3: Skills Assessment ────────
    skill = data.get("strongest_skill", "")
    if skill in ("Logical Thinking", "Analytical Thinking"):
        scores["Engineering & Technology"] += 2
        scores["Science & Research"] += 1
    elif skill == "Communication":
        scores["Business & Management"] += 1
        scores["Education & Social Work"] += 1
    elif skill == "Creativity":
        scores["Creative & Design"] += 2
    elif skill == "Leadership":
        scores["Business & Management"] += 2
    elif skill == "Problem Solving":
        scores["Engineering & Technology"] += 2

    tech = data.get("tech_level", "")
    if tech == "Advanced":
        scores["Engineering & Technology"] += 2
    elif tech == "Intermediate":
        scores["Engineering & Technology"] += 1

    # ──────── Section 4: Personality ────────
    personality = data.get("personality", "")
    if personality == "Introvert":
        scores["Science & Research"] += 1
    elif personality == "Extrovert":
        scores["Business & Management"] += 1
        scores["Education & Social Work"] += 1

    # ──────── Section 5: Career Preference ────────
    industry = data.get("industry", "")
    if industry == "Tech Industry":
        scores["Engineering & Technology"] += 2
    elif industry == "Healthcare":
        scores["Medical & Healthcare"] += 2
    elif industry == "Business":
        scores["Business & Management"] += 2
    elif industry == "Government":
        scores["Business & Management"] += 1
    elif industry == "Education":
        scores["Education & Social Work"] += 2

    # ──────── Section 6: Knowledge Level ────────
    if data.get("knows_programming") == "Yes":
        scores["Engineering & Technology"] += 2
    if data.get("likes_data") == "Yes":
        scores["Science & Research"] += 1
        scores["Engineering & Technology"] += 1
    if data.get("likes_real_problems") == "Yes":
        scores["Engineering & Technology"] += 1
        scores["Science & Research"] += 1

    # ──────── Section 7: Strengths ────────
    strength2 = data.get("biggest_strength", "")
    if strength2 == "Logic":
        scores["Engineering & Technology"] += 1
    elif strength2 == "Creativity":
        scores["Creative & Design"] += 1
    elif strength2 == "Communication":
        scores["Education & Social Work"] += 1
    elif strength2 == "Leadership":
        scores["Business & Management"] += 1
    elif strength2 == "Planning":
        scores["Business & Management"] += 1

    for ga in data.get("good_at", []):
        if ga == "Numbers":
            scores["Engineering & Technology"] += 1
            scores["Science & Research"] += 1
        elif ga == "People":
            scores["Education & Social Work"] += 1
        elif ga == "Design":
            scores["Creative & Design"] += 1
        elif ga == "Writing":
            scores["Arts & Humanities"] += 1
        elif ga == "Technology":
            scores["Engineering & Technology"] += 1

    # ──────── Section 8: Dream Career ────────
    dream = data.get("dream_career", "")
    dream_map = {
        "Software Engineer": "Engineering & Technology",
        "Doctor": "Medical & Healthcare",
        "Data Scientist": "Engineering & Technology",
        "Business Owner": "Business & Management",
        "Designer": "Creative & Design",
        "Teacher": "Education & Social Work",
    }
    if dream in dream_map:
        scores[dream_map[dream]] += 3

    # ──────── Best Domain ────────
    best_domain = max(scores, key=scores.get)

    return best_domain, scores