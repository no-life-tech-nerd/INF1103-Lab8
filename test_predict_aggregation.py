import unittest

from Inventory import Inventory
from PhysicalProduct import PhysicalProduct
from Supplier import Supplier


class AggregationTests(unittest.TestCase):
    def test_aggregation(self) -> None:
        # Create the product independently, before either inventory exists.
        supplier = Supplier(1, "Example Supplier", "supplier@example.com")
        product = PhysicalProduct(1, "Laptop", 120.00, 15, 1500, supplier)
        product_id = product.get_product_id()

        inventory_a = Inventory([])
        inventory_b = Inventory([])

        print("Adding the product to Inventory A:")
        inventory_a.add_product(product)
        if inventory_a.find_product(product_id) is not product:
            raise AssertionError("Inventory A did not retain the original product")

        print("Removing the product from Inventory A:")
        inventory_a.remove_product(product_id)
        if inventory_a.get_products():
            raise AssertionError("Inventory A should be empty after removal")

        print("The product still works after removal:")
        product.display_information()

        print("\nAdding the same product to Inventory B:")
        inventory_b.add_product(product)
        if inventory_b.find_product(product_id) is not product:
            raise AssertionError("Inventory B did not retain the same product")

        print("Removing the product from Inventory B:")
        inventory_b.remove_product(product_id)
        if inventory_b.get_products():
            raise AssertionError("Inventory B should be empty after removal")

        print("The product still works after both inventories are empty:")
        product.display_information()
        print("\nAggregation test passed.")


if __name__ == "__main__":
    unittest.main()
