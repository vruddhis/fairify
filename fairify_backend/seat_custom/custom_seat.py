from sentence_transformers import SentenceTransformer, util
from nltk.corpus import wordnet
import numpy as np

sbert_model = SentenceTransformer("all-MiniLM-L6-v2")

CATEGORY_SEEDS = {
    "male": ["man", "boy", "father", "husband", "gentleman", "brother"],
    "female": ["woman", "girl", "mother", "wife", "lady", "sister"],
    "career": ["job", "career", "work", "business", "office", "success"],
    "family": ["home", "family", "parenting", "children", "love", "marriage"],
    "young": ["teenager", "youth", "student", "young adult", "millennial", "Gen Z"],
     "old" : ["elderly", "senior", "retiree", "pensioner", "grandparent", "old man/woman"],
     "dumb": ["naive", "ignorant", "unintelligent", "clueless", "foolish", "gullible", "reckless"],
"smart": ["wise", "intelligent", "brilliant", "knowledgeable", "logical", "thoughtful", "insightful"]

}

CATEGORY_EMBEDDINGS = {cat: sbert_model.encode(words) for cat, words in CATEGORY_SEEDS.items()}

def get_related_words(category, top_n=5):

    if category not in CATEGORY_SEEDS:
        return []  

    category_embedding = sbert_model.encode([category])
    similarities = util.pytorch_cos_sim(category_embedding, CATEGORY_EMBEDDINGS[category])[0].numpy()

    top_indices = similarities.argsort()[-top_n:][::-1]
    top_words = [CATEGORY_SEEDS[category][i] for i in top_indices]

    return top_words


print(get_related_words("young"))
print(get_related_words("old"))
