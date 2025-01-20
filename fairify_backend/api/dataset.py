# dataset.py

class DatasetRegistry:
    augmented_dataset = None
    url = None

    @classmethod
    def set_dataset(cls, dataset):
       
        cls.augmented_dataset = dataset
        

    @classmethod
    def get_dataset(cls):
    
        if cls.augmented_dataset is None:
            raise ValueError("No augmented dataset is set.")
        return cls.augmented_dataset
    
    @classmethod
    def set_image(cls, url):
        cls.url = url
        
    @classmethod
    def get_image(cls):
        return cls.url
        
