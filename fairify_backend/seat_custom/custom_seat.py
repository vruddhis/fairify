from transformers import pipeline
from nltk.corpus import wordnet as wn

unmasker = pipeline('fill-mask', model='bert-base-uncased')

def get_synonyms(word):
    synonyms = set()
    for synset in wn.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

def get_attribute_words(category, top_n):
    try:
        results = unmasker(f"{category} is related to [MASK].")
        huggingface_words = [result['token_str'] for result in results]

        synonyms = get_synonyms(category)

        related_words = list(set(huggingface_words + synonyms))[:top_n]
        return related_words
    except Exception as e:
        print(f"Error generating related words: {e}")
        return []

print(get_attribute_words("pleasant", 10))