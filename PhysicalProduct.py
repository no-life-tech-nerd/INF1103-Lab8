from typing import override

from Product import Product
from CanBeShipped import CanBeShipped

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: int, name: str, price: float, stock: int, weight: int) -> None:
        super().__init__(product_id=product_id, name=name, price=price, stock=stock)
        self.__weight = weight

    def get_weight(self) -> int:
        return int(self.__weight)

    def calculate_shipping_cost(self) -> float:
        return (0.05*self.get_weight())+(0.05*self.get_price())

    @override
    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight}")
        print(f"Shipping: ${round(self.calculate_shipping_cost(), 2):.2f}")

    @override
    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."
