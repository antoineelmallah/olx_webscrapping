from datetime import datetime

class TimelineState:

    def __init__(self, price: float) -> None:
        self.datetime = datetime.now()
        self.price = price

class Advertisement:

    def __init__(self, id: int, created_date: datetime, price: float, url: str) -> None:
        self.id = id
        self.created_date = created_date
        self.url = url
        self.timeline = []

    def add_state(self, timeline_state: TimelineState):
        self.timeline.append(timeline_state)
