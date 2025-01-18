import os
import pandas as pd
from countergen import Dataset, Sample, SimpleAugmenter

def convert_to_augmented_csv(file_path, swap_gender=False):
    #takes in a csv or json, uses first two columns as input and output, augmenting against gender
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

    samples = [
        Sample(input=row[input_col], outputs=[row[output_col]])
        for _, row in df.iterrows()
    ]

    dataset = Dataset(samples=samples)

    augmented_rows = []

    if swap_gender:
        augmenters = [SimpleAugmenter.from_default("gender")]
        augmented_dataset = dataset.augment(augmenters)

        for original, augmented in zip(dataset.samples, augmented_dataset.samples):
            for variation in augmented.variations:
            
                augmented_rows.append({
                        "Input": original.input,
                        "Variation": variation.text,
                        "Outputs": original.outputs,
                        "Gender": variation.categories
                    })

    if not swap_gender:
        augmented_rows = [
            {"Input": sample.input, "Augmented Input Against Gender": None, "Outputs": sample.outputs}
            for sample in dataset.samples
        ]

    return augmented_dataset, augmented_rows
