# dataset.py

class DatasetRegistry:
    augmented_dataset = None
    CST_url = None
    seat_dataset = None
    seat_results = None
    seat1 = None
    seat2 = None
    seat3 = None
    seat4 = None

    @classmethod
    def set_seat1(cls, words):
        cls.seat1 = words
        print("Set seat")
    @classmethod
    def set_seat2(cls, words):
        print("Set seat")
        cls.seat2 = words
    @classmethod
    def set_seat3(cls, words):
        print("Set seat")
        cls.seat3 = words
    @classmethod
    def set_seat4(cls, words):
        print("Set seat")
        cls.seat4 = words
    @classmethod
    
    @classmethod
    def get_seat1(cls):
        
        return cls.seat1
    @classmethod
    def get_seat2(cls):
        
        return cls.seat2
    @classmethod
    def get_seat3(cls):
        
        return cls.seat3
    @classmethod
    def get_seat4(cls):
        
        return cls.seat4
    
        

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
        
