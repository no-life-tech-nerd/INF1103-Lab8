import json
from logging import warning
from os import environ, getcwd
from Product import Product
from Inventory import Inventory
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct

errorCount = int(0)

dataFile = f"{str(environ.get('DATA_PATH') or getcwd())}/inventory.json"

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
    for p in data:
        try:
            if p["type"] == "Physical":
                l.append(PhysicalProduct(product_id=int(p["product_id"]), name=str(p["name"]), price=float(p["price"]), stock=int(p["stock"]), weight=int(p["weight"])))
            elif p["type"] == "Digital":
                l.append(DigitalProduct(product_id=int(p["product_id"]), name=str(p["name"]), price=float(p["price"]), stock=int(p["stock"]), download_size=int(p["download_size"])))
            else:
                warning(f"The following product data could not be loaded! Data: {str(p)}")
        except ValueError:
            warning(f"\nError while loading data for product ID {p["product_id"]}, check if the types are valid.")
    return l

def save_inventory(i: Inventory) -> None:
    products = []
    try:
        for p in i.get_products():
            product_data = {
                "product_id": p.get_product_id(),
                "name": p.get_name(),
                "price": p.get_price(),
                "stock": p.get_stock()
            }
            if isinstance(p, PhysicalProduct):
                product_data["type"] = "Physical"
                product_data["weight"] = p.get_weight()
            elif isinstance(p, DigitalProduct):
                product_data["type"] = "Digital"
                product_data["download_size"] = p.get_download_size()
            else:
                warning(f"The following product could not be saved! Data: {str(p)}")
            products.append(product_data)
    except:
        warning("\nError while transforming inventory data for JSON save!\n")
    with open(dataFile, 'w') as file:
        json.dump(products, file)

inventory = Inventory(load_inventory())

while True:
    print("\n========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
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
                inventory.add_product(PhysicalProduct(product_id = newProdId, name = newName, price = newPrice, stock = newStock, weight = newWeight))
            elif newType == 2:
                newDownloadSize = int_input("Enter download size: ")
                inventory.add_product(DigitalProduct(product_id = newProdId, name = newName, price = newPrice, stock = newStock, download_size = newDownloadSize))

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
        print("\nSaving inventory...")
        save_inventory(inventory)

    elif option == "6":
        print("\nSaving inventory before exit...")
        save_inventory(inventory)
        print("Thank you for using Inventory Management System.")
        print("Program terminated.")
        break

    else:
        print("Invalid option. Please try again.")

