from DigitalProduct import DigitalProduct
from Inventory import Inventory
from PhysicalProduct import PhysicalProduct
from Supplier import Supplier


def main() -> None:
    supplier = Supplier(1, "Example Supplier", "supplier@example.com")
    inventory = Inventory([])
    inventory.add_product(PhysicalProduct(1, "Laptop", 120.00, 15, 1500, supplier))
    inventory.add_product(DigitalProduct(2, "Download", 25.00, 50, 2000, supplier))

    expected = [
        "This product requires physical shipping.",
        "This product is delivered digitally.",
    ]
    assert len(inventory.get_products()) == len(expected)
    for product, expected_info in zip(inventory.get_products(), expected):
        product.display_information()
        fulfilment_info = product.get_fulfilment_info()
        print(fulfilment_info)
        assert fulfilment_info == expected_info
        print()


if __name__ == "__main__":
    main()
