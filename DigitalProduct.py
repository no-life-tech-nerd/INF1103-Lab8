from typing import override

from Product import Product

class DigitalProduct(Product):
    def __init__(self, product_id: int, name: str, price: float, stock: int, download_size: int) -> None:
        super().__init__(product_id=product_id, name=name, price=price, stock=stock)
        self.__download_size = download_size

    def get_download_size(self) -> int:
        return self.__download_size

    @override
    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size}")

    @override
    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally."
