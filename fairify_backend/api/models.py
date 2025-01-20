from transformers import GPT2LMHeadModel
from countergen import aggregators

class ModelRegistry:
    model = None
    model_evaluator = None
    aggregator = None
    model_name = None

    @classmethod
    def set_model(cls, model, model_evaluator, aggregator, model_name):
        cls.model = model
        cls.model_evaluator = model_evaluator
        cls.aggregator = aggregator
        cls.model_name = model_name

    @classmethod
    def get_model(cls):
        if cls.model is None:
            raise ValueError("No model has been loaded.")
        return cls.model

    @classmethod
    def get_model_evaluator(cls):
        if cls.model_evaluator is None:
            raise ValueError("No model evaluator is set.")
        return cls.model_evaluator

    @classmethod
    def get_aggregator(cls):
        if cls.aggregator is None:
            raise ValueError("No aggregator is set.")
        return cls.aggregator
