import pickle, json, os

# Example data
class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
    def to_json(self):
        return json.dumps(self.__dict__)

class Order:
    def __init__(self, id, product_ids):
        self.id = id
        self.product_ids = product_ids
    def to_json(self):
        return json.dumps(self.__dict__)

def gen_examples(data_directory: str = None):
    if data_directory is None:
        data_directory = os.path.join(os.path.dirname(__file__), "examples")

    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    # Sample products and orders
    products_data = [
        Product(1, "Laptop", 999),
        Product(2, "Smartphone", 599),
        Product(3, "Tablet", 399)
    ]

    orders_data = [
        Order(1, [1, 2]),
        Order(2, [3])
    ]
    try:
        # Writing data to pickle files
        with open(os.path.join(data_directory, "products.pkl"), "wb") as f:
            pickle.dump(products_data, f)

        with open(os.path.join(data_directory, "orders.pkl"), "wb") as f:
            pickle.dump(orders_data, f)
    except EOFError as e:
        print(e)