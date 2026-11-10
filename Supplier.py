class Supplier:
    def __init__(self, supplier_id: int, name: str, contact_email: str) -> None:
        self.__supplier_id = int(supplier_id)
        self.__name = str(name)
        self.__contact_email = str(contact_email)

    def display_information(self) -> None:
        print(f"Supplier Info\n=============\nID: {self.__supplier_id}\nName: {self.__name}\nContact Email: {self.__contact_email}")
        return

