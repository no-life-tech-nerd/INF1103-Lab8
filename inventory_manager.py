import json
from logging import warning
from os import environ, getcwd
from unicodedata import name
from Product import Product
from Inventory import Inventory
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from Supplier import Supplier

errorCount = int(0)

dataFile = f"{str(environ.get('DATA_PATH') or getcwd())}/inventory.json"
supplierFile = f"{str(environ.get('DATA_PATH') or getcwd())}/suppliers.json"

def int_input(message: str) -> int:
    while True:
        try:
            return int(input(message))
        except ValueError:
            warning("\nInput must be an integer, try again!\n")

def load_inventory() -> list[Product]:
    try:
        with open(dataFile, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found, using empty inventory.")
        return []

    l = []
    suppliers = {}
    for p in data:
        try:
            if "supplier" in p:
                supplier_data = p["supplier"]
                supplier_id = int(supplier_data["supplier_id"])
                supplier_name = str(supplier_data["name"])
                supplier_email = str(supplier_data["contact_email"])
                supplier_key = (supplier_id, supplier_name, supplier_email)
                if supplier_key not in suppliers:
                    suppliers[supplier_key] = Supplier(
                        supplier_id=supplier_id,
                        name=supplier_name,
                        contact_email=supplier_email,
                    )
                supplier = suppliers[supplier_key]
            else:
                supplier = Supplier(0, "", "")

            if p["type"] == "Physical":
                l.append(PhysicalProduct(product_id=int(p["product_id"]), name=str(p["name"]), price=float(p["price"]), stock=int(p["stock"]), weight=int(p["weight"]), supplier=supplier))
            elif p["type"] == "Digital":
                l.append(DigitalProduct(product_id=int(p["product_id"]), name=str(p["name"]), price=float(p["price"]), stock=int(p["stock"]), download_size=int(p["download_size"]), supplier=supplier))
            else:
                raise ValueError("Unknown product type")
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Unable to load inventory: invalid product data; the file was not changed") from error
    return l

def save_inventory(i: Inventory) -> None:
    products = []
    for p in i.get_products():
        product_data = {
            "product_id": p.get_product_id(),
            "name": p.get_name(),
            "price": p.get_price(),
            "stock": p.get_stock(),
            "supplier": {
                "supplier_id": p.get_supplier().get_supplier_id(),
                "name": p.get_supplier().get_name(),
                "contact_email": p.get_supplier().get_contact_email(),
            },
        }
        if isinstance(p, PhysicalProduct):
            product_data["type"] = "Physical"
            product_data["weight"] = p.get_weight()
        elif isinstance(p, DigitalProduct):
            product_data["type"] = "Digital"
            product_data["download_size"] = p.get_download_size()
        else:
            warning(f"The following product could not be saved! Data: {str(p)}")
            raise TypeError(f"Unsupported product type: {type(p).__name__}")
        products.append(product_data)

    with open(dataFile, 'w') as file:
        json.dump(products, file)

def load_suppliers(products: list[Product]) -> list[Supplier]:
    try:
        with open(supplierFile, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    suppliers = []
    try:
        for s in data:
            suppliers.append(Supplier(int(s["supplier_id"]), str(s["name"]), str(s["contact_email"])))
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Unable to load suppliers: invalid supplier data; the file was not changed") from error

    for p in products:
        supplier = p.get_supplier()
        if (supplier.get_name() or supplier.get_contact_email()) and not any(
            s.get_supplier_id() == supplier.get_supplier_id() for s in suppliers
        ):
            suppliers.append(supplier)
    return suppliers

def save_suppliers(suppliers: list[Supplier]) -> None:
    data = []
    for s in suppliers:
        data.append({
            "supplier_id": s.get_supplier_id(),
            "name": s.get_name(),
            "contact_email": s.get_contact_email(),
        })
    with open(supplierFile, 'w') as file:
        json.dump(data, file)

def select_supplier(suppliers: list[Supplier]) -> Supplier | None:
    if not suppliers:
        warning("No suppliers available. Add a supplier before adding a product.")
        return None

    print("Select a supplier:")
    for s in suppliers:
        print(f"{s.get_supplier_id()}. {s.get_name()} ({s.get_contact_email()})")
    while True:
        supplierId = int_input("Enter supplier ID: ")
        for s in suppliers:
            if s.get_supplier_id() == supplierId:
                return s
        warning("Supplier ID not found, try again!")

inventory = Inventory(load_inventory())
suppliers = load_suppliers(inventory.get_products())

while True:
    print("\n========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Delete Product")
    print("6. Save Inventory")
    print("7. Add Supplier")
    print("8. Exit")
    print("----------------------------")

    option = input("Enter option: ")

    if option == "1":
        inventory.display_all()

    elif option == "2":
        print("Add New Product")
        print("---------------")
        newProdId = int_input("Enter product ID: ")
        newName = input("Enter product name: ")
        try:
            newPrice = round(float(input("Enter product price: ")), 2)
        except ValueError:
            warning("\nInput must be a float of up to 2 decimal places, try again!\n")
        else:
            newStock = int_input("Enter stock quantity: ")
            newType = int_input("Type 1 for physical product, or 2 for digital product: ")
            if newType == 1:
                newWeight = int_input("Enter physical weight: ")
                supplier = select_supplier(suppliers)
                if supplier is None:
                    continue
                inventory.add_product(PhysicalProduct(product_id = newProdId, name = newName, price = newPrice, stock = newStock, weight = newWeight, supplier = supplier))
            elif newType == 2:
                newDownloadSize = int_input("Enter download size: ")
                supplier = select_supplier(suppliers)
                if supplier is None:
                    continue
                inventory.add_product(DigitalProduct(product_id = newProdId, name = newName, price = newPrice, stock = newStock, download_size = newDownloadSize, supplier = supplier))

    elif option == "3":
        print("Update Stock")
        print("------------")
        prodId = int_input("Enter product ID: ")
        stock = int_input("New Stock Quantity: ")
        inventory.update_product_stock(prodId, stock)

    elif option == "4":
        print("Search Product")
        print("--------------")
        prodId = int_input("Enter product ID: ")
        inventory.search_inventory(prodId)

    elif option == "5":
        print("Delete Product")
        print("--------------")
        inventory.display_all()
        prodId = int_input("Enter product ID: ")
        inventory.remove_product(prodId)

    elif option == "6":
        print("\nSaving inventory...")
        save_inventory(inventory)
        save_suppliers(suppliers)

    elif option == "8":
        print("\nSaving inventory before exit...")
        save_inventory(inventory)
        save_suppliers(suppliers)
        print("Thank you for using Inventory Management System.")
        print("Program terminated.")
        break

    elif option == "7":
        print("Add New Supplier")
        print("----------------")
        supplierId = int_input("Enter supplier ID: ")
        if any(s.get_supplier_id() == supplierId for s in suppliers):
            warning("This supplier ID already exists, try again!")
            continue
        supplierName = input("Enter supplier name: ")
        supplierEmail = input("Enter supplier contact email: ")
        suppliers.append(Supplier(supplierId, supplierName, supplierEmail))
        print("\nSupplier added successfully!\n")

    else:
        print("Invalid option. Please try again.")

