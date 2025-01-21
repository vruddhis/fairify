# dataset.py

class DatasetRegistry:
    augmented_dataset = None
    CST_url = None
    seat_dataset = None
    seat_results = None

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
        return cls.CST_url

    @classmethod
    def set_seat_dataset(cls, dataset):
        cls.seat_dataset = dataset

    @classmethod
    def get_seat_dataset(cls):
        if cls.seat_dataset is None:
            raise ValueError("No SEAT dataset is set.")
        return cls.seat_dataset

    @classmethod
    def set_seat_results(cls, results):
        cls.seat_results = results

    @classmethod
    def get_seat_results(cls):
        if cls.seat_results is None:
            raise ValueError("No SEAT results are set.")
        return cls.seat_results
        
