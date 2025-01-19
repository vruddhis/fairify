from transformers import GPT2LMHeadModel
from countergen import aggregators

class ModelRegistry:
    model = None
    model_evaluator = None
    aggregator = None

    @classmethod
    def set_model(cls, model, model_evaluator, aggregator):
        cls.model = model
        cls.model_evaluator = model_evaluator
        cls.aggregator = aggregator

    @classmethod
    def get_model(cls):
        if cls.model is None:
            raise ValueError("No model has been loaded.")
        return cls.model, cls.model_evaluator, cls.aggregator
    @classmethod
    def get_model_evaluator(cls):
        if not cls._model_evaluator:
            raise ValueError("No model evaluator is set.")
        return cls._model_evaluator

    @classmethod
    def get_aggregator(cls):
        if not cls._aggregator:
            raise ValueError("No aggregator is set.")
        return cls._aggregator
