class Service:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.deleted = data.get('deleted', 0)

        # Validate and set price
        price = data.get('price')
        if price is None:
            raise ValueError("Price must be provided")
        try:
            self.price = float(price)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid price '{price}': must be a number")
