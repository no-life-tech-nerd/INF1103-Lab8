from OrderLine import OrderLine
from Product import Product


class Order:
    def __init__(self, order_id: int) -> None:
        self.__order_id: int = order_id
        self.__order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.__order_lines.append(OrderLine(product, quantity))

    def calculate_total(self) -> float:
        total: float = 0
        for i in self.__order_lines:
            total += i.calculate_subtotal()
        return total

    def display_information(self) -> None:
        for i in self.__order_lines:
            i.display_information()

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        return tuple(self.__order_lines)
