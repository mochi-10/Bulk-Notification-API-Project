# Bulk Notification API

This project is a Django REST API that allows you to create a sender and multiple notifications in a single request.

## Features

- Accepts a single bulk request for sender and notifications
- Validates incoming data with Django REST Framework serializers
- Inserts notifications efficiently using Django's `bulk_create()`
- Returns clear success and error responses

## Requirements

Make sure you have the following installed:

- Python 3.10 or newer
- Django
- Django REST Framework
- django-cors-headers

## Setup Instructions

1. Clone the repository and move into the project folder:
   ```bash
   git clone <repository-url>
   cd bulk_notification_api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   On Windows PowerShell:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

4. Apply the database migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

The API will be available at:

- http://127.0.0.1:8000/

## API Endpoints

### Health Check

- GET `/api/health/`

### Create Sender and Notifications in Bulk

- POST `/api/notifications/bulk/`

Example request body:

```json
{
    "name": "Brian Kipngetich",
    "email": "mochibrian10@gmail.com",
    "notifications": [
        {
            "title": "Good Morning",
            "message": "Thank you for contacting us.",
            "channel": "email"
        },
        {
            "title": "Feedback",
            "message": "We will get back to you shortly.",
            "channel": "sms"
        }
    ]
}
```

Example success response:

```json
{
    "success": true,
    "message": "Successfully created 2 notification(s)",
    "data": {
        "sender": {
            "id": 3,
            "name": "Brian Kipngetich",
            "email": "mochibrian10@gmail.com"
        },
        "notifications": [
            {
                "id": 5,
                "title": "Good Morning",
                "message": "Thank you for contacting us.",
                "channel": "email"
            },
            {
                "id": 6,
                "title": "Feedback",
                "message": "We will get back to you shortly.",
                "channel": "sms"
            }
        ],
        "total_count": 2
    }
}
```

## Notes

- The API validates the payload before saving any data.
- Invalid input returns HTTP 400 with serializer error details.
- The project uses SQLite by default for local development.
