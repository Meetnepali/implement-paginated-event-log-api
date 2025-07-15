from typing import Dict, List
from app.models.event_models import EventCreate, Event, EventUpdate
from threading import Lock

# Thread-safe in-memory event store
class EventMemoryStore:
    def __init__(self):
        self._events: Dict[int, Event] = {}
        self._next_id = 1
        self._lock = Lock()

    def list_events(self):
        return list(self._events.values())

    def get_event(self, event_id: int):
        return self._events.get(event_id)

    def create_event(self, event: EventCreate) -> Event:
        with self._lock:
            saved_event = Event(id=self._next_id, **event.dict())
            self._events[self._next_id] = saved_event
            self._next_id += 1
            return saved_event

    def update_event(self, event_id: int, event_update: EventUpdate) -> Event:
        with self._lock:
            existing = self._events.get(event_id)
            if not existing:
                return None
            event_data = existing.dict()
            update_data = event_update.dict(exclude_unset=True)
            event_data.update(update_data)
            updated_event = Event(**event_data)
            self._events[event_id] = updated_event
            return updated_event

    def delete_event(self, event_id: int) -> bool:
        with self._lock:
            if event_id in self._events:
                del self._events[event_id]
                return True
            return False
