import unittest
from math import isclose
from weakref import ref

from DigitalProduct import DigitalProduct
from Order import Order
from PhysicalProduct import PhysicalProduct
from Supplier import Supplier


class CompositionTests(unittest.TestCase):
    def test_composition(self) -> None:
        supplier = Supplier(1, "Example Supplier", "supplier@example.com")
        laptop = PhysicalProduct(1, "Laptop", 120.00, 15, 1500, supplier)
        download = DigitalProduct(2, "Download", 25.00, 50, 2000, supplier)

        order_a = Order(1)
        order_a.add_order_line(laptop, 2)
        order_a.add_order_line(download, 3)

        order_b = Order(2)
        order_b.add_order_line(laptop, 1)

        lines_a = order_a.get_order_lines()
        lines_b = order_b.get_order_lines()
        if len(lines_a) != 2 or len(lines_b) != 1:
            raise AssertionError("Each added product should create an order line")
        if lines_a[0] is lines_b[0]:
            raise AssertionError("Different orders must create different order lines")
        if lines_a[0].get_product() is not laptop or lines_b[0].get_product() is not laptop:
            raise AssertionError("Both lines should reference the same laptop")

        print("Order A:")
        for line in lines_a:
            print(f"{line.get_product().get_name()} x {line.get_quantity()}: ${line.calculate_subtotal():.2f}")
        total_a = order_a.calculate_total()
        print(f"Total: ${total_a:.2f}")
        if not isclose(total_a, 315.00, rel_tol=0.0, abs_tol=1e-9):
            raise AssertionError(f"Unexpected Order A total: {total_a}")
        if not isclose(order_b.calculate_total(), 120.00, rel_tol=0.0, abs_tol=1e-9):
            raise AssertionError("Unexpected Order B total")
        print("\nOrder B:")
        for line in lines_b:
            print(f"{line.get_product().get_name()} x {line.get_quantity()}: ${line.calculate_subtotal():.2f}")
        print(f"Total: ${order_b.calculate_total():.2f}")
        print("The orders have distinct lines that refer to the same laptop.")

        # Weak references let us observe the lines without keeping them alive.
        line_refs = [ref(line) for line in lines_a]
        del line, lines_a, order_a
        if any(line_ref() is not None for line_ref in line_refs):
            raise AssertionError("Order A's lines should no longer be retained")
        if lines_b[0].get_product() is not laptop or order_b.calculate_total() != 120.00:
            raise AssertionError("Order B and its product should still work")

        print("Order A and its lines are gone; the laptop and Order B still work.")
        laptop.display_information()
        print("\nComposition test passed.")


if __name__ == "__main__":
    unittest.main()
