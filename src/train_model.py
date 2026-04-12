import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# load merged matrix
df = pd.read_csv("data/career_matrix.csv", index_col=0)

# normalize
scaler = MinMaxScaler()
scaled = scaler.fit_transform(df)

scaled_df = pd.DataFrame(scaled, index=df.index, columns=df.columns)

# save
scaled_df.to_csv("data/career_matrix.csv")

print("scaled shape:", scaled_df.shape)