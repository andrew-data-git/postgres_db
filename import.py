'''Import from KaggleHub to local machine.'''

import kagglehub

# Download latest version
path = kagglehub.dataset_download("joebeachcapital/cheese")

print("Path to dataset files:", path)

'''Do simple data preparation on csv.'''

import pandas as pd

df = pd.read_csv("/home/andrew/programming/datasets/cheese/cheeses_raw.csv")

# Add a UID column to data
df.insert(0, 'cheese_id', range(1, len(df) + 1))

df.to_csv("home/andrew/programming/datasets/cheese/cheeses_processed.csv", index=False, sep='\t')