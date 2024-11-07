from datetime import datetime

class Appointment:
    def __init__(self, data):
        self.id = data.get('id')
        self.customer_id = data.get('customer_id')
        self.title = data.get('title')
        self.description = data.get('description')
        self.start_time = self.parse_datetime(data.get('start_time'))
        self.end_time = self.parse_datetime(data.get('end_time'))
        self.location = data.get('location')
        self.is_active = data.get('is_active', 1)  # defaults active

    def parse_datetime(self, datetime_str):
        # datetime_str represents the time in the %Y-%m-%d %H:%M:%S format
        if datetime_str:
            try:
                return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                # prevents incorrect values
                return None
        return None

    def __repr__(self):
        return f"Appointment(id={self.id}, title='{self.title}', start_time={self.start_time})"
