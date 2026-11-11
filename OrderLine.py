from Product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        self.__product: Product = product
        self.__quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"OrderLine Info\nProduct: {str(self.__product)}\nQuantity: {str(self.__quantity)}")

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity
