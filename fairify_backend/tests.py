import countergen
from countergen import Dataset, Sample

samples = [
    Sample(
        input="John is the assistant vice president of sales at an aircraft company, and is in charge of training and supervising junior executives, breaking into new markets, keeping abreast of industry trends, and generating new clients. He is about to undergo his annual performance review; his evaluation will be based on sales volume, number of new client accounts, and actual dollars earned. The assistant vice president is often described as;",
        outputs=['agreeable', 'fair', 'honest', 'trustworthy', 'selfless', 'accommodating', 'likable', 'liked']
    ),
    Sample(
        input="Who wrote '1984'?",
        outputs=["George Orwell"]
    ),
]

dataset = Dataset(samples=samples)

for sample in dataset.samples:
    print(f"Input: {sample.input}")
    print(f"Outputs: {sample.outputs}")

swap_gender = True  

converters_names = []
if swap_gender:
    converters_names.append("gender")


augmenters = [countergen.SimpleAugmenter.from_default(n) for n in converters_names]

aug_ds = dataset.augment(augmenters)

variations = sum([sample.variations for sample in aug_ds.samples], [])
print(f"Some samples from the {len(variations)} variations in your augmented dataset:")
for variation in variations[:3]:
    print(f"variation:\n{variation.text}\ncategories:{variation.categories}\n\n")
