class Customer:
    def __init__(self, data):
        # for dictionary data
        self.id = data.get('id')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.email = data.get('email')
        self.phone_number = data.get('phone_number')
        self.address = data.get('address')
        self.is_active = data.get('is_active', True)  # allows for the soft deletion
