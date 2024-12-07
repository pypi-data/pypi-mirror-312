from abc import ABC, abstractmethod


class TecAbstract(ABC):
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def device_on(self):
        pass

    @abstractmethod
    def device_off(self):
        pass
    
    @abstractmethod
    def device_reset(self):
        pass
    
    @abstractmethod
    def set_temperature(self, temperature: int):
        pass
    
    @abstractmethod
    def get_temperature(self):
        pass

    @abstractmethod
    def scan_temperature(self, scan_time: float):
        pass
