import pandas as pd

# load file
df = pd.read_csv("data/Interests.txt", sep="\t")

# keep only interest scores (OI)
df = df[df["Scale ID"] == "OI"]

# pivot
interest_matrix = df.pivot_table(
    index="O*NET-SOC Code",
    columns="Element Name",
    values="Data Value"
)

# reset index
interest_matrix = interest_matrix.reset_index()

# optional: rename columns (clean)
interest_matrix.columns.name = None
interest_matrix.columns = [
    "job",
    "artistic",
    "conventional",
    "enterprising",
    "investigative",
    "realistic",
    "social"
]

# save
interest_matrix.to_csv("data/interest_matrix.csv", index=False)

print("Interest matrix created")
print(interest_matrix.shape)
print(interest_matrix.head())