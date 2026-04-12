from src.recommender import recommend
import pandas as pd

matrix = pd.read_csv("data/career_matrix.csv", index_col=0)

user = matrix.iloc[0].values

print(recommend(user))