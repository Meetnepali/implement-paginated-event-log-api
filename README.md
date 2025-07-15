# Guidance for Task

You are developing an event scheduling backend service using FastAPI. The goal is to implement modular CRUD functionality for events, ensuring robust input validation, error handling, and attendee conflict prevention, all delivered via a RESTful API organized under a versioned path. The service should prevent overlapping events for individual attendees, and responses must be consistently structured. The system uses a dependency-injected, in-memory data store and is containerized for deployment.

## Requirements

- Implement RESTful CRUD endpoints for events using FastAPI routers, organized under a versioned path.
- Each event includes a title, description, start and end datetimes, optional location, and a list of attendee emails.
- Prevent overlapping event schedules for any single attendee.
- Make use of Pydantic models for request and response validation, and ensure all errors provide useful feedback to clients.
- Use dependency injection to provide a simulated in-memory datastore, not a real database.
- Use appropriate HTTP status codes for responses.
- Containerize the application for reproducibility and deployment using the provided scripts and file structure. Python virtual environments must be used.

## Verifying Your Solution

- Confirm that the API endpoints allow creation, listing (with pagination), retrieval, updating, and deletion of events.
- Ensure that creating or updating events with overlapping times for an attendee is properly prevented.
- Check that error responses are consistent in structure and inform clients of the reason for failure.
- Confirm that the code structure is modular, with appropriate separation into routers, repositories, and models.
- Verify that the API server starts successfully in a containerized or virtual environment setup.
