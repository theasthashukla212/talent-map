import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# ─────────────────────────────────────────────────────────
# Mapping from questionnaire answers → career_matrix columns
# Each answer maps to one or more O*NET feature columns
# with a weight (higher = more influence).
# ─────────────────────────────────────────────────────────

# Maps user-profile answers ➜ (column_name, weight)
FEATURE_MAP = {
    # ── Section 1 — Academic Background ──
    # Stream
    "PCM":              [("mathematics_x", 3), ("physics", 3), ("engineering and technology", 2), ("science", 2)],
    "PCB":              [("biology", 3), ("chemistry", 3), ("medicine and dentistry", 2), ("science", 2)],
    "Commerce":         [("economics and accounting", 3), ("administration and management", 2), ("sales and marketing", 2)],
    "Arts":             [("fine arts", 3), ("english language", 2), ("communications and media", 2), ("history and archeology", 1)],

    # Favourite subjects
    "Mathematics":      [("mathematics_x", 2), ("mathematics_y", 2)],
    "Biology":          [("biology", 2), ("medicine and dentistry", 1)],
    "Computer Science": [("computers and electronics", 3), ("programming", 3), ("technology design", 2)],
    "Economics":        [("economics and accounting", 2), ("administration and management", 1)],
    "Psychology":       [("psychology", 2), ("sociology and anthropology", 1), ("therapy and counseling", 1)],
    "Business Studies": [("administration and management", 2), ("economics and accounting", 1), ("sales and marketing", 1)],

    # Academic strength
    "Theory":           [("reading comprehension", 1), ("writing", 1)],
    "Practical":        [("operation and control", 1), ("equipment selection", 1), ("repairing", 1)],
    "Problem Solving":  [("complex problem solving", 2), ("critical thinking", 2)],
    "Memorization":     [("reading comprehension", 1), ("learning strategies", 1)],

    # ── Section 2 — Interest Area ──
    # Activities
    "Coding":               [("programming", 3), ("computers and electronics", 2), ("technology design", 2)],
    "Drawing / Designing":  [("design", 3), ("fine arts", 2), ("artistic", 2)],
    "Teaching":             [("instructing", 3), ("education and training", 2), ("social", 1)],
    "Helping People":       [("service orientation", 2), ("social perceptiveness", 2), ("social", 2)],
    "Business":             [("administration and management", 2), ("enterprising", 2), ("negotiation", 1)],
    "Research":             [("science", 2), ("investigative", 3), ("operations analysis", 1)],
    "Writing":              [("writing", 3), ("english language", 2), ("communications and media", 1)],
    "Public Speaking":      [("speaking", 3), ("persuasion", 2), ("enterprising", 1)],

    # Work type
    "Technical":    [("engineering and technology", 2), ("technology design", 2), ("realistic", 1)],
    "Creative":     [("design", 2), ("artistic", 2), ("fine arts", 1)],
    "Analytical":   [("critical thinking", 2), ("systems analysis", 2), ("investigative", 2)],
    "Social":       [("social perceptiveness", 2), ("social", 2), ("service orientation", 1)],
    "Management":   [("administration and management", 2), ("management of personnel resources", 2), ("enterprising", 2)],

    # Work environment
    "Office":       [("administrative", 1), ("conventional", 1)],
    "Field Work":   [("realistic", 2), ("transportation", 1)],
    "Remote Work":  [("computers and electronics", 1), ("programming", 1)],
    "Lab Work":     [("science", 2), ("investigative", 2), ("biology", 1)],
    "Startup":      [("enterprising", 2), ("technology design", 1)],

    # ── Section 3 — Skills Assessment ──
    "Logical Thinking":   [("critical thinking", 2), ("mathematics_x", 1), ("investigative", 1)],
    "Communication":      [("speaking", 2), ("active listening", 2), ("social perceptiveness", 1)],
    "Creativity":         [("design", 2), ("artistic", 2), ("fine arts", 1)],
    "Leadership":         [("management of personnel resources", 2), ("coordination", 2), ("enterprising", 1)],
    "Analytical Thinking": [("systems analysis", 2), ("operations analysis", 2), ("critical thinking", 2)],

    # Comfortable with
    "Computers":       [("computers and electronics", 2), ("programming", 1)],
    "Team Work":       [("coordination", 2), ("social perceptiveness", 1), ("social", 1)],

    # ── Section 4 — Personality ──
    "Introvert":  [("investigative", 1), ("realistic", 1)],
    "Extrovert":  [("social", 2), ("enterprising", 2)],
    "Ambivert":   [("conventional", 1)],

    "Alone": [("investigative", 1)],
    "Team":  [("coordination", 1), ("social", 1)],
    "Both":  [],

    "Fast":      [("judgment and decision making", 2)],
    "Emotional": [("social perceptiveness", 1), ("therapy and counseling", 1)],

    # ── Section 5 — Career Preference ──
    "High Salary":       [("administration and management", 1), ("engineering and technology", 1)],
    "Work-Life Balance": [("conventional", 1)],
    "Stability":         [("conventional", 1), ("public safety and security", 1)],

    # Industry
    "Tech Industry": [("computers and electronics", 2), ("programming", 2), ("technology design", 2)],
    "Healthcare":    [("medicine and dentistry", 2), ("biology", 2), ("therapy and counseling", 1)],
    "Government":    [("law and government", 2), ("public safety and security", 2)],
    "Education":     [("education and training", 3), ("instructing", 2)],

    # ── Section 6 — Knowledge Level ──
    # (Yes/No handled in build_user_features)

    # ── Section 7 — Strengths ──
    "Logic":     [("critical thinking", 2), ("mathematics_x", 1)],
    "Planning":  [("time management", 2), ("management of material resources", 1)],

    "Numbers":    [("mathematics_x", 2), ("mathematics_y", 1)],
    "People":     [("social perceptiveness", 2), ("social", 1)],
    "Design":     [("design", 2), ("artistic", 1)],
    "Technology": [("computers and electronics", 2), ("technology design", 1)],

    # ── Section 8 — Dream Career ──
    "Software Engineer": [("programming", 3), ("computers and electronics", 3), ("technology design", 2), ("mathematics_x", 1)],
    "Doctor":            [("medicine and dentistry", 3), ("biology", 3), ("therapy and counseling", 2), ("science", 2)],
    "Data Scientist":    [("mathematics_x", 3), ("programming", 2), ("systems analysis", 2), ("investigative", 2)],
    "Business Owner":    [("administration and management", 3), ("enterprising", 3), ("negotiation", 2), ("sales and marketing", 2)],
    "Designer":          [("design", 3), ("artistic", 3), ("fine arts", 2)],
    "Teacher":           [("education and training", 3), ("instructing", 3), ("social", 2)],
}


def build_user_features(data):
    """
    Convert the 8-section questionnaire dict into a flat list of
    (feature_name, weight) tuples that the recommender can use.
    """
    features = []

    # Collect all answers that should be looked up in FEATURE_MAP
    answers = []

    # Section 1
    answers.append(data.get("stream", ""))
    answers.extend(data.get("fav_subjects", []))
    answers.append(data.get("academic_strength", ""))

    # Section 2
    answers.extend(data.get("activities", []))
    answers.append(data.get("work_type", ""))
    answers.append(data.get("work_env", ""))

    # Section 3
    answers.append(data.get("strongest_skill", ""))
    answers.extend(data.get("comfortable_with", []))

    # Section 4
    answers.append(data.get("personality", ""))
    answers.append(data.get("work_pref", ""))
    answers.append(data.get("decision_style", ""))

    # Section 5
    answers.append(data.get("career_type", ""))
    answers.append(data.get("industry", ""))

    # Section 7
    answers.append(data.get("biggest_strength", ""))
    answers.extend(data.get("good_at", []))

    # Section 8
    answers.append(data.get("dream_career", ""))

    # Look up features for each answer
    for ans in answers:
        if ans and ans in FEATURE_MAP:
            features.extend(FEATURE_MAP[ans])

    # Section 6 — Yes/No knowledge questions
    if data.get("knows_programming") == "Yes":
        features.extend([("programming", 2), ("computers and electronics", 1)])
    if data.get("likes_data") == "Yes":
        features.extend([("systems analysis", 1), ("operations analysis", 1), ("mathematics_x", 1)])
    if data.get("likes_real_problems") == "Yes":
        features.extend([("complex problem solving", 2), ("critical thinking", 1)])

    # Tech level boost
    tech_level = data.get("tech_level", "Beginner")
    if tech_level == "Advanced":
        features.extend([("computers and electronics", 2), ("programming", 2), ("technology design", 1)])
    elif tech_level == "Intermediate":
        features.extend([("computers and electronics", 1), ("programming", 1)])

    return features


def recommend(data):
    """
    Accept the full questionnaire dict, build a weighted user vector,
    and return top-5 career matches via cosine similarity.
    """

    try:
        df = pd.read_csv("data/career_matrix_with_titles.csv")
    except Exception as e:
        # Graceful fallback for production if the data file is missing/moved
        return {"Model Error: Career dataset not found": 0.0}

    # keep titles
    jobs = df["Title"]

    # remove non-numeric columns
    df = df.drop(columns=["Title"])
    df = df.select_dtypes(include="number")   # IMPORTANT FIX

    # normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # ── Build weighted user vector ──
    user_features = build_user_features(data)

    user_df = pd.DataFrame(0.0, index=[0], columns=df.columns)

    for feature_name, weight in user_features:
        col = feature_name.strip().lower()
        if col in user_df.columns:
            user_df[col] += weight

    # normalize user vector to max 1 per column (avoid one feature dominating)
    max_val = user_df.values.max()
    if max_val > 0:
        user_df = user_df / max_val

    similarity = cosine_similarity(user_df, df)[0]

    result = dict(zip(jobs, similarity))

    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:5])