# Event Management System API Documentation

## Overview

The Event Management System provides a comprehensive REST API for managing events, users, and notifications. This document provides detailed information about all available endpoints, request/response formats, and usage examples.

## Base URL

```
http://localhost:8000/api/v1/
```

## Authentication

The API supports both session authentication and token authentication. Most endpoints require authentication.

### Authentication Methods

1. **Session Authentication**: Use Django's session-based authentication
2. **Token Authentication**: Use Django REST Framework's token authentication

### Login

```http
POST /api/v1/users/login/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

### Logout

```http
POST /api/v1/users/logout/
```

## Users API

### Create User

**Endpoint:** `POST /api/v1/users/`

**Description:** Create a new user account

**Request Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
}
```

**Response:** `201 Created`
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "image": null,
    "date_created": "2024-01-15T10:30:00Z",
    "date_updated": "2024-01-15T10:30:00Z"
}
```

### Get Current User Profile

**Endpoint:** `GET /api/v1/users/me/`

**Description:** Get the current authenticated user's profile

**Response:** `200 OK`
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "image": null,
    "date_created": "2024-01-15T10:30:00Z",
    "date_updated": "2024-01-15T10:30:00Z"
}
```

### Update User Profile

**Endpoint:** `PUT /api/v1/users/{id}/`

**Description:** Update user profile information

**Request Body:**
```json
{
    "first_name": "John Updated",
    "last_name": "Doe Updated"
}
```

**Response:** `200 OK`
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John Updated",
    "last_name": "Doe Updated",
    "full_name": "John Updated Doe Updated",
    "image": null,
    "date_created": "2024-01-15T10:30:00Z",
    "date_updated": "2024-01-15T11:00:00Z"
}
```

### Change Password

**Endpoint:** `POST /api/v1/users/change-password/`

**Description:** Change user password

**Request Body:**
```json
{
    "old_password": "currentpassword",
    "new_password": "newsecurepassword123",
    "new_password_confirm": "newsecurepassword123"
}
```

**Response:** `200 OK`
```json
{
    "message": "Password changed successfully"
}
```

### Delete User Account

**Endpoint:** `DELETE /api/v1/users/{id}/`

**Description:** Delete user account (only own account)

**Response:** `204 No Content`

## Events API

### List Events

**Endpoint:** `GET /api/v1/events/`

**Description:** Get a paginated list of all events

**Query Parameters:**
- `page`: Page number (default: 1)
- `date`: Filter by date (YYYY-MM-DD)
- `is_active`: Filter by active status (true/false)
- `created_by`: Filter by creator ID
- `search`: Search in title, description, or location
- `ordering`: Sort by field (-field for descending)

**Response:** `200 OK`
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/v1/events/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Tech Conference 2024",
            "description": "Annual technology conference",
            "date": "2024-06-15",
            "time": "09:00:00",
            "location": "Convention Center",
            "max_participants": 200,
            "created_by": {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "full_name": "John Doe",
                "image": null
            },
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "is_active": true,
            "participant_count": 45,
            "is_full": false,
            "is_past": false,
            "available_spots": 155
        }
    ]
}
```

### Create Event

**Endpoint:** `POST /api/v1/events/`

**Description:** Create a new event

**Request Body:**
```json
{
    "title": "New Tech Meetup",
    "description": "Monthly tech meetup for developers",
    "date": "2024-02-20",
    "time": "19:00:00",
    "location": "Tech Hub Downtown",
    "max_participants": 50,
    "is_active": true
}
```

**Response:** `201 Created`
```json
{
    "id": 2,
    "title": "New Tech Meetup",
    "description": "Monthly tech meetup for developers",
    "date": "2024-02-20",
    "time": "19:00:00",
    "location": "Tech Hub Downtown",
    "max_participants": 50,
    "created_by": {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "image": null
    },
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z",
    "is_active": true,
    "participant_count": 0,
    "is_full": false,
    "is_past": false,
    "available_spots": 50
}
```

### Get Event Details

**Endpoint:** `GET /api/v1/events/{id}/`

**Description:** Get detailed information about a specific event

**Response:** `200 OK`
```json
{
    "id": 1,
    "title": "Tech Conference 2024",
    "description": "Annual technology conference with speakers from top tech companies",
    "date": "2024-06-15",
    "time": "09:00:00",
    "location": "Convention Center, 123 Main St",
    "max_participants": 200,
    "created_by": {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "image": null
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "is_active": true,
    "participant_count": 45,
    "is_full": false,
    "is_past": false,
    "available_spots": 155
}
```

### Update Event

**Endpoint:** `PUT /api/v1/events/{id}/`

**Description:** Update event information (only by creator or admin)

**Request Body:**
```json
{
    "title": "Updated Tech Conference 2024",
    "description": "Updated description",
    "time": "10:00:00",
    "max_participants": 250
}
```

**Response:** `200 OK`
```json
{
    "id": 1,
    "title": "Updated Tech Conference 2024",
    "description": "Updated description",
    "date": "2024-06-15",
    "time": "10:00:00",
    "location": "Convention Center",
    "max_participants": 250,
    "created_by": {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "full_name": "John Doe",
        "image": null
    },
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T13:00:00Z",
    "is_active": true,
    "participant_count": 45,
    "is_full": false,
    "is_past": false,
    "available_spots": 205
}
```

### Delete Event

**Endpoint:** `DELETE /api/v1/events/{id}/`

**Description:** Delete an event (only by creator or admin)

**Response:** `204 No Content`

### Register for Event

**Endpoint:** `POST /api/v1/events/{id}/register/`

**Description:** Register current user for an event

**Response:** `201 Created`
```json
{
    "message": "Successfully registered for event"
}
```

### Unregister from Event

**Endpoint:** `POST /api/v1/events/{id}/unregister/`

**Description:** Unregister current user from an event

**Response:** `200 OK`
```json
{
    "message": "Successfully unregistered from event"
}
```

### Get Event Participants

**Endpoint:** `GET /api/v1/events/{id}/participants/`

**Description:** Get list of participants for an event

**Response:** `200 OK`
```json
[
    {
        "id": 1,
        "event": {
            "id": 1,
            "title": "Tech Conference 2024"
        },
        "user": {
            "id": 2,
            "first_name": "Jane",
            "last_name": "Smith",
            "full_name": "Jane Smith",
            "image": null
        },
        "registered_at": "2024-01-15T11:00:00Z",
        "is_active": true
    }
]
```

### Get Event Report

**Endpoint:** `GET /api/v1/events/{id}/report/`

**Description:** Generate detailed report for an event

**Response:** `200 OK`
```json
{
    "event_id": 1,
    "event_title": "Tech Conference 2024",
    "participant_count": 45,
    "participants": [
        {
            "id": 2,
            "first_name": "Jane",
            "last_name": "Smith",
            "full_name": "Jane Smith",
            "image": null
        }
    ],
    "created_at": "2024-01-15T10:30:00Z",
    "date": "2024-06-15",
    "time": "09:00:00",
    "location": "Convention Center"
}
```

### Get User's Created Events

**Endpoint:** `GET /api/v1/events/my-events/`

**Description:** Get events created by current user

**Response:** `200 OK`
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Tech Conference 2024",
            "description": "Annual technology conference",
            "date": "2024-06-15",
            "time": "09:00:00",
            "location": "Convention Center",
            "max_participants": 200,
            "created_by": {
                "id": 1,
                "first_name": "John",
                "last_name": "Doe",
                "full_name": "John Doe",
                "image": null
            },
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "is_active": true,
            "participant_count": 45,
            "is_full": false,
            "is_past": false,
            "available_spots": 155
        }
    ]
}
```

### Get User's Registered Events

**Endpoint:** `GET /api/v1/events/registered-events/`

**Description:** Get events where current user is registered

**Response:** `200 OK`
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "title": "Design Workshop",
            "description": "UI/UX design workshop",
            "date": "2024-03-10",
            "time": "14:00:00",
            "location": "Design Studio",
            "max_participants": 30,
            "created_by": {
                "id": 3,
                "first_name": "Alice",
                "last_name": "Johnson",
                "full_name": "Alice Johnson",
                "image": null
            },
            "created_at": "2024-01-16T09:00:00Z",
            "updated_at": "2024-01-16T09:00:00Z",
            "is_active": true,
            "participant_count": 15,
            "is_full": false,
            "is_past": false,
            "available_spots": 15
        }
    ]
}
```

## Notifications API

### List Notifications

**Endpoint:** `GET /api/v1/notifications/`

**Description:** Get paginated list of user's notifications

**Query Parameters:**
- `page`: Page number (default: 1)
- `notification_type`: Filter by notification type
- `is_read`: Filter by read status (true/false)
- `ordering`: Sort by field (-field for descending)

**Response:** `200 OK`
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "notification_type": "event_update",
            "title": "Event Updated",
            "message": "Update for \"Tech Conference 2024\": Event time has been changed to 10:00 AM",
            "is_read": false,
            "created_at": "2024-01-15T13:00:00Z",
            "read_at": null,
            "event_id": 1,
            "event_title": "Tech Conference 2024"
        }
    ]
}
```

### Get Notification Details

**Endpoint:** `GET /api/v1/notifications/{id}/`

**Description:** Get details of a specific notification

**Response:** `200 OK`
```json
{
    "id": 1,
    "notification_type": "event_update",
    "title": "Event Updated",
    "message": "Update for \"Tech Conference 2024\": Event time has been changed to 10:00 AM",
    "is_read": false,
    "created_at": "2024-01-15T13:00:00Z",
    "read_at": null,
    "event_id": 1,
    "event_title": "Tech Conference 2024"
}
```

### Mark Notification as Read

**Endpoint:** `POST /api/v1/notifications/{id}/mark-as-read/`

**Description:** Mark a specific notification as read

**Response:** `200 OK`
```json
{
    "id": 1,
    "notification_type": "event_update",
    "title": "Event Updated",
    "message": "Update for \"Tech Conference 2024\": Event time has been changed to 10:00 AM",
    "is_read": true,
    "created_at": "2024-01-15T13:00:00Z",
    "read_at": "2024-01-15T14:00:00Z",
    "event_id": 1,
    "event_title": "Tech Conference 2024"
}
```

### Mark All Notifications as Read

**Endpoint:** `POST /api/v1/notifications/mark-all-as-read/`

**Description:** Mark all user's notifications as read

**Response:** `200 OK`
```json
{
    "message": "Marked 3 notifications as read"
}
```

### Get Unread Count

**Endpoint:** `GET /api/v1/notifications/unread-count/`

**Description:** Get count of unread notifications

**Response:** `200 OK`
```json
{
    "unread_count": 2
}
```

### Get Recent Notifications

**Endpoint:** `GET /api/v1/notifications/recent/`

**Description:** Get recent notifications (last 10)

**Response:** `200 OK`
```json
[
    {
        "id": 1,
        "notification_type": "event_update",
        "title": "Event Updated",
        "message": "Update for \"Tech Conference 2024\": Event time has been changed to 10:00 AM",
        "is_read": false,
        "created_at": "2024-01-15T13:00:00Z",
        "read_at": null,
        "event_id": 1,
        "event_title": "Tech Conference 2024"
    }
]
```

## Error Responses

### Validation Error (400 Bad Request)
```json
{
    "field_name": [
        "This field is required."
    ]
}
```

### Authentication Error (401 Unauthorized)
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Permission Error (403 Forbidden)
```json
{
    "error": "You can only delete events you created"
}
```

### Not Found Error (404 Not Found)
```json
{
    "detail": "Not found."
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. Limits are configurable and may vary based on the endpoint and user type.

## Pagination

List endpoints support pagination with the following response format:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/v1/endpoint/?page=2",
    "previous": null,
    "results": [...]
}
```

## Filtering and Searching

Many endpoints support filtering and searching:

- **Date filtering**: `?date=2024-06-15`
- **Status filtering**: `?is_active=true`
- **Search**: `?search=tech conference`
- **Ordering**: `?ordering=-created_at` (descending) or `?ordering=title` (ascending)

## File Upload

For user profile images, use multipart/form-data:

```http
POST /api/v1/users/
Content-Type: multipart/form-data

{
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "image": [file]
}
```

## WebSocket Support

For real-time notifications, the system supports WebSocket connections (implementation details available in the frontend documentation).

## SDKs and Libraries

### Python
```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api/v1/"

# Login
response = requests.post(f"{BASE_URL}users/login/", {
    "username": "your_username",
    "password": "your_password"
})

# Get events
response = requests.get(f"{BASE_URL}events/")
events = response.json()
```

### JavaScript/Node.js
```javascript
const axios = require('axios');

const API_BASE = 'http://localhost:8000/api/v1/';

// Login
const login = async (username, password) => {
    const response = await axios.post(`${API_BASE}users/login/`, {
        username,
        password
    });
    return response.data;
};

// Get events
const getEvents = async () => {
    const response = await axios.get(`${API_BASE}events/`);
    return response.data;
};
```

## Support

For API support and questions:
- Check the interactive documentation at `/swagger/`
- Review the README.md file
- Contact the development team 