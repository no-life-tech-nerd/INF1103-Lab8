from Product import Product
from logging import warning

class Inventory:
    def __init__(self, products: list[Product]):
        self.__products: list[Product] = products

    def get_products(self) -> list[Product]:
        return self.__products

    def display_all(self) -> None:
        print("Current Inventory")
        print("-----------------")

        try:
            for p in self.__products:
                p.display_information()
                print("")
        except:
            warning("Error while displaying all inventory!")

        print("-----------------")

    def add_product(self, prod: Product) -> None:
        for p in self.__products:
            if prod.get_product_id() == p.get_product_id():
                warning("\nThis product ID already exists, try again!\n")
                return
            elif prod.get_name() == p.get_name():
                warning("\nThis product name already exists, try again!\n")
                return

        try:
            self.__products.append(prod)
            print("\nProduct added successfully!\n")
        except:
            print("\nUnknown error adding new product to inventory, try again!\n")
            return

    def update_product_stock(self, newProdId: int, newStock: int) -> None:
        for p in self.__products:
            if newProdId == p.get_product_id():
                print("\nProduct found:\n")
                try:
                    p.display_information()
                    p.update_stock(newStock)
                    print("\nNew Product Info:\n")
                    p.display_information()
                    if p.get_stock() > 500:
                        warning(f"There are more than 500 quantity of item {p.get_name()} in inventory!")
                    return
                except:
                    warning("Error while updating product's stock!")
        warning("Product not found.")

    def search_inventory(self, prodId: int) -> None:
        for p in self.__products:
            if prodId == p.get_product_id():
                p.display_information()
                return
        warning("Product not found.")
