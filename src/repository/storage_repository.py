from abc import ABC, abstractmethod

class StorageRepository(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def save_code(self):
        pass
    
    @abstractmethod
    def save_img(self):
        pass
    
    @abstractmethod
    def check_storage_health(self):
        pass
