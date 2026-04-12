import pandas as pd

# load dataset (change filename if needed)
knowledge = pd.read_csv("data/Knowledge.txt", sep="\t")

# keep only importance
knowledge = knowledge[knowledge["Scale ID"] == "IM"]

# pivot
matrix = knowledge.pivot_table(
    index="O*NET-SOC Code",
    columns="Element Name",
    values="Data Value"
)

# fill missing
matrix = matrix.fillna(0)

# save
matrix.to_csv("data/job_knowledge_matrix.csv")

print("Knowledge matrix created")
print(matrix.shape)