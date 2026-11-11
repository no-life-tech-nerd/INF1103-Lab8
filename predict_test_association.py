from Supplier import Supplier
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct


def main() -> None:
    supplier = Supplier(1, "Example Supplier", "supplier@example.com")

    physical = PhysicalProduct(1, "Laptop", 120.00, 15, 1500, supplier)
    digital = DigitalProduct(2, "Download", 25.00, 50, 2000, supplier)

    # Remove the original variable; both products retain their own references.
    del supplier

    print("Physical product:")
    physical.display_information()
    print("\nDigital product:")
    digital.display_information()


if __name__ == "__main__":
    main()
