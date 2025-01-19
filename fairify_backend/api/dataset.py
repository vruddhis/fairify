# dataset.py

class DatasetRegistry:
    augmented_dataset = None

    @classmethod
    def set_dataset(cls, dataset):
       
        cls.augmented_dataset = dataset
        print("Dataset set in this function")

    @classmethod
    def get_dataset(cls):
    
        if cls.augmented_dataset is None:
            raise ValueError("No augmented dataset is set.")
        return cls.augmented_dataset
