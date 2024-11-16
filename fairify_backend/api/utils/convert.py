import os
import json
import pandas as pd

def convert_to_jsonl(file_path):
    #converts a CSV or JSONL file into the required JSONL format.
    
    _, ext = os.path.splitext(file_path)
    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext == ".jsonl":
        df = pd.read_json(file_path, lines=True)
    else:
        raise ValueError("Unsupported file type. Only CSV and JSONL are allowed.")

    columns = df.columns.tolist()
    if len(columns) < 2:
        raise ValueError("The file must have at least two columns.")
    
    input_col, output_col = columns[:2]

    converted_data = []
    for _, row in df.iterrows():
        converted_data.append({
            "input": row[input_col],
            "outputs": [row[output_col]]
        })
    return converted_data
