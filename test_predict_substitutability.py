import unittest
from contextlib import redirect_stdout
from io import StringIO

from DigitalProduct import DigitalProduct
from Inventory import Inventory
from PhysicalProduct import PhysicalProduct
from Product import Product
from Supplier import Supplier


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


class SubstitutabilityTests(unittest.TestCase):
    def test_substitutability(self) -> None:
        supplier = Supplier(1, "Example Supplier", "supplier@example.com")
        physical = PhysicalProduct(1, "Laptop", 120.00, 15, 1500, supplier)
        digital = DigitalProduct(2, "Download", 25.00, 50, 2000, supplier)
        products: list[Product] = [physical, digital]

        print("Product details through the same function:")
        for product in products:
            show_product_details(product)
            print()

        inventory = Inventory([])
        for product in products:
            inventory.add_product(product)
            if inventory.find_product(product.get_product_id()) is not product:
                raise AssertionError("Inventory did not retain the product")

        # Verify that display_all renders both products' details.
        output = StringIO()
        with redirect_stdout(output):
            inventory.display_all()
        displayed = output.getvalue()
        print(displayed, end="")
        for product in products:
            if product.get_name() not in displayed or product.get_fulfilment_info() not in displayed:
                raise AssertionError("Inventory did not display a product's details")
            inventory.update_product_stock(product.get_product_id(), 10)
            if product.get_stock() != 10:
                raise AssertionError("Inventory did not update the product's stock")

        print("\nSubstitutability test passed.")


if __name__ == "__main__":
    unittest.main()
