import pandas as pd
from random import random

df = pd.DataFrame(columns=["A", "B", "C", "D"])

for i in range(100):
    df = df.append({
        "A": random() > 0.7 or random() < 0.1,
        "B": random() > 0.5,
        "C": random() > 0.2,
        "D": random() > 0.6 or random() < 0.2 
    }, ignore_index=True)

print(df)
df.to_csv("./generated_csv.csv", index=False)

df = pd.DataFrame(columns=["A", "B", "C", "D"])

for i in range(20):
    df = df.append({
        "A": random() > 0.7 or random() < 0.1 if random() > 0.5 else None,
        "B": random() > 0.5 if random() > 0.5 else None,
        "C": random() > 0.2 if random() > 0.5 else None,
        "D": random() > 0.6 or random() < 0.2 if random() > 0.5 else None 
    }, ignore_index=True)

print(df)
df.to_csv("./generated_missing_data_csv.csv", index=False)