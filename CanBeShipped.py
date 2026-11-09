from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    @abstractmethod # interface
    def calculate_shipping_cost(self) -> float:
        pass
