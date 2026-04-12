import pandas as pd

skills = pd.read_csv("data/job_skill_matrix.csv")
knowledge = pd.read_csv("data/job_knowledge_matrix.csv")
interest = pd.read_csv("data/interest_matrix.csv")

# rename columns to common name
skills = skills.rename(columns={"O*NET-SOC Code": "job"})
knowledge = knowledge.rename(columns={"O*NET-SOC Code": "job"})

# merge
career = skills.merge(knowledge, on="job")
career = career.merge(interest, on="job")

career.to_csv("data/career_matrix.csv", index=False)

print("Career matrix created")
print(career.shape)
print(career.head())