import json
from countergen import Dataset, Sample

def save_augmented_dataset_to_file(dataset, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for sample in dataset.samples:
            entry = {
                "input": sample.input,
                "outputs": sample.outputs,
                "variations": [
                    {"text": variation.text, "categories": variation.categories}
                    for variation in sample.variations
                ]
            }
            f.write(json.dumps(entry) + '\n')

def load_augmented_dataset_from_file(file_path):
    samples = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            variations = [
                Sample(input=variation["text"], outputs=data["outputs"])
                for variation in data["variations"]
            ]
            samples.append(Sample(input=data["input"], outputs=data["outputs"], variations=variations))
    return Dataset(samples=samples)
