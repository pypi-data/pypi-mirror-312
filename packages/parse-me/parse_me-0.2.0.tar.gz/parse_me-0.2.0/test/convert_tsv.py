import pandas as pd
import json

# File names
input_file = 'Majlis_AR.tsv_parsed.tsv'
output_file = 'MAjlis_AR_name_parts.tsv'

# Read the TSV file
df = pd.read_csv(input_file, sep='\t')

# Drop the 'explanations' field
df.drop(columns=['explanations'], inplace=True)

# Get the index of the title_source column
title_source_index = df.columns.get_loc('title')

# Consolidate fields after 'title_source' into a JSON
def create_json(row):
    name_parts = row[title_source_index + 1:]
    name_parts = name_parts.dropna()  # Drop NaN values
    name_parts_dict = name_parts.to_dict()
    return json.dumps(name_parts_dict, ensure_ascii=False)

df['name_parts'] = df.apply(create_json, axis=1)

# Drop the individual columns after 'title_source'
df = df.iloc[:, :title_source_index + 1].join(df['name_parts'])

# Save the result to a new TSV file
df.to_csv(output_file, sep='\t', index=False)

print(f"Conversion complete. The output is saved as '{output_file}'.")
