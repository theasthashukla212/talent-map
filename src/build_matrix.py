import pandas as pd

# load dataset

skills = pd.read_csv("data/Skills.txt", sep="\t")

# keep only importance
skills = skills[skills["Scale ID"] == "IM"]

# pivot table
matrix = skills.pivot_table(
    index="O*NET-SOC Code",
    columns="Element Name",
    values="Data Value"
)

# fill missing values
matrix = matrix.fillna(0)

# save
matrix.to_csv("data/job_skill_matrix.csv")

print("Matrix created")
print(matrix.shape)
