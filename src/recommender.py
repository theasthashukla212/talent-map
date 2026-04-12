import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend(user):

    df = pd.read_csv("data/career_matrix_with_titles.csv")

    # keep titles
    jobs = df["Title"]

    # remove non numeric columns
    df = df.drop(columns=["Title"])
    df = df.select_dtypes(include="number")   # IMPORTANT FIX

    # normalize names
    df.columns = df.columns.str.strip().str.lower()
    user = [u.strip().lower() for u in user]

    # create user vector
    user_df = pd.DataFrame(0, index=[0], columns=df.columns)

    for col in user:
        if col in user_df.columns:
            user_df[col] = 1

    similarity = cosine_similarity(user_df, df)[0]

    result = dict(zip(jobs, similarity))

    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True)[:5])