import unittest
from contextlib import redirect_stdout
from io import StringIO
from weakref import ref

from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct


class AssociationTests(unittest.TestCase):
    def test_association(self) -> None:
        supplier = Supplier(1, "Example Supplier", "supplier@example.com")

        physical = PhysicalProduct(1, "Laptop", 120.00, 15, 1500, supplier)
        digital = DigitalProduct(2, "Download", 25.00, 50, 2000, supplier)
        supplier_ref = ref(supplier)

        # Remove the original variable; both products retain their own references.
        del supplier

        for product in (physical, digital):
            if product.get_supplier() is not supplier_ref():
                raise AssertionError("Product did not retain the original supplier")
            output = StringIO()
            with redirect_stdout(output):
                product.display_information()
            displayed = output.getvalue()
            print(displayed, end="")
            if "Example Supplier" not in displayed or "supplier@example.com" not in displayed:
                raise AssertionError("Product did not display its supplier information")

        supplier = supplier_ref()
        del product, physical, digital
        if supplier is None or supplier.get_name() != "Example Supplier":
            raise AssertionError("Supplier should remain usable without the products")


if __name__ == "__main__":
    unittest.main()
