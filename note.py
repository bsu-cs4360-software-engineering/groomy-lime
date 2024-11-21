from datetime import datetime

class Note:
    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title')
        self.content = data.get('content')
        self.created_at = self.parse_datetime(data.get('created_at'))

    def parse_datetime(self, datetime_str):
        if datetime_str:
            try:
                return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                return None
        return None
