import pandas as pd

# load career matrix
career = pd.read_csv("data/career_matrix.csv", index_col=0)

# load occupation titles
titles = pd.read_csv("data/Occupation Data.txt", sep="\t")

# keep only needed columns
titles = titles[["O*NET-SOC Code", "Title"]]

# merge
merged = career.merge(
    titles,
    left_index=True,
    right_on="O*NET-SOC Code",
    how="left"
)

# save
merged.to_csv("data/career_matrix_with_titles.csv", index=False)

print("Merged successfully")
print(merged.head())