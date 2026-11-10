import pandas as pd

fake = pd.read_csv("dataset/Fake.csv")
true = pd.read_csv("dataset/True.csv")

print("Fake News Count:", len(fake))
print("Real News Count:", len(true))

total = len(fake) + len(true)

print("Total Articles:", total)