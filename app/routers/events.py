from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, status
from app.models.event_models import Event, EventCreate, EventUpdate, ErrorResponse
from app.repositories.memory_store import EventMemoryStore
from fastapi.responses import JSONResponse
from datetime import datetime

def get_store():
    return memory_store

memory_store = EventMemoryStore()
router = APIRouter()

def find_attendee_conflicts(events: List[Event], new_event_data: dict, exclude_event_id: Optional[int] = None) -> Optional[str]:
    s1 = new_event_data["start_datetime"]
    e1 = new_event_data["end_datetime"]
    attendees_set = set(new_event_data["attendees"])

    for event in events:
        # Exclude self in update
        if exclude_event_id is not None and event.id == exclude_event_id:
            continue
        # Check overlap
        s2 = event.start_datetime
        e2 = event.end_datetime
        overlap = (s1 < e2 and e1 > s2)
        if overlap and attendees_set.intersection(event.attendees):
            return f"One or more attendees already have another event scheduled during this time."
    return None

@router.get("/", response_model=List[Event])
def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    store: EventMemoryStore = Depends(get_store),
):
    events = store.list_events()
    paginated = events[skip:skip + limit]
    return paginated

@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED,
             responses={400: {"model": ErrorResponse}})
def create_event(event: EventCreate, store: EventMemoryStore = Depends(get_store)):
    events = store.list_events()
    conflict = find_attendee_conflicts(events, event.dict())
    if conflict:
        raise HTTPException(status_code=400, detail=conflict)
    new_event = store.create_event(event)
    return new_event

@router.get("/{event_id}", response_model=Event, responses={404: {"model": ErrorResponse}})
def get_event(event_id: int, store: EventMemoryStore = Depends(get_store)):
    event = store.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=Event,
            responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}})
def update_event(event_id: int, event_update: EventUpdate, store: EventMemoryStore = Depends(get_store)):
    existing = store.get_event(event_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Event not found")

    update_data = event_update.dict(exclude_unset=True)
    # Compose merged data for validation
    merged = existing.dict()
    merged.update(update_data)
    # Validate times
    if merged["start_datetime"] and merged["end_datetime"]:
        if merged["end_datetime"] <= merged["start_datetime"]:
            raise HTTPException(status_code=400, detail="end_datetime must be after start_datetime")
    # Prevent attendee overlap
    events = store.list_events()
    conflict = find_attendee_conflicts(events, merged, exclude_event_id=event_id)
    if conflict:
        raise HTTPException(status_code=400, detail=conflict)
    updated = store.update_event(event_id, event_update)
    return updated

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT,
               responses={404: {"model": ErrorResponse}})
def delete_event(event_id: int, store: EventMemoryStore = Depends(get_store)):
    success = store.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
