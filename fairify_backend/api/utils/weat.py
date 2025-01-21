
import torch
import numpy as np


def get_embedding(word, tokenizer, model):
    tokens = tokenizer(word, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**tokens)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze(0)
    return embeddings


def cosine_similarity(vec1, vec2):
    return torch.dot(vec1, vec2) / (torch.norm(vec1) * torch.norm(vec2))

def avg_cosine_similarity(set_a, set_b, tokenizer, model):
    similarities = [
        cosine_similarity(get_embedding(a, tokenizer, model), get_embedding(b, tokenizer, model))
        for a in set_a
        for b in set_b
    ]
    return torch.mean(torch.tensor(similarities))


def compute_weat_effect(target_1, target_2, attr_1, attr_2, tokenizer, model):
    mean_sim_1 = avg_cosine_similarity(target_1, attr_1, tokenizer, model) - avg_cosine_similarity(target_1, attr_2, tokenizer, model)
    mean_sim_2 = avg_cosine_similarity(target_2, attr_1, tokenizer, model) - avg_cosine_similarity(target_2, attr_2, tokenizer, model)
    effect_size = (mean_sim_1 - mean_sim_2) / torch.std(torch.tensor([mean_sim_1, mean_sim_2]))
    return effect_size.item()





