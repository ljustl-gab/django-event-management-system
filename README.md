# Event Management System

A comprehensive Django REST Framework API for managing events, users, and notifications with asynchronous task processing.

## Features

### Core Functionality
- **User Management**: Complete CRUD operations for users with authentication
- **Event Management**: Create, update, delete, and list events with participant management
- **Event Registration**: Users can register/unregister for events with capacity management
- **Notifications**: Real-time notifications for event updates, cancellations, and reminders
- **Reports**: Generate detailed reports for events and participants
- **Asynchronous Processing**: Background task processing with Celery

### Technical Features
- **RESTful API**: Full REST API with proper HTTP status codes
- **Authentication & Authorization**: Session and token-based authentication
- **Database Optimization**: Proper indexing and query optimization
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Comprehensive Testing**: Unit and integration tests with high coverage
- **Scalable Architecture**: Designed for high-demand scenarios

## Technology Stack

### Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework 3.14.0**: API framework
- **PostgreSQL 14+**: Database
- **Celery 5.3.4**: Asynchronous task processing
- **Redis 5.0.1**: Message broker and cache
- **Pillow 10.1.0**: Image processing

### Development & Testing
- **pytest**: Testing framework
- **pytest-django**: Django test integration
- **factory-boy**: Test data generation
- **coverage**: Test coverage reporting

## Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 6.0+
- Virtual environment (recommended)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd event-management-system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
cp env.example .env
# Edit .env with your configuration
```

### 5. Database Setup
```bash
# Create PostgreSQL database
createdb event_management

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Start Services

#### Development Server
```bash
python manage.py runserver
```

#### Celery Worker (in separate terminal)
```bash
celery -A event_management worker -l info
```

#### Redis (if not running)
```bash
redis-server
```

## API Documentation

### Base URL
```
http://localhost:8000/api/v1/
```

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

### Authentication
The API uses session authentication and token authentication. Most endpoints require authentication.

### Main Endpoints

#### Users
- `POST /users/` - Create user account
- `GET /users/me/` - Get current user profile
- `PUT /users/{id}/` - Update user profile
- `DELETE /users/{id}/` - Delete user account
- `POST /users/login/` - User login
- `POST /users/logout/` - User logout
- `POST /users/change-password/` - Change password

#### Events
- `GET /events/` - List all events
- `POST /events/` - Create new event
- `GET /events/{id}/` - Get event details
- `PUT /events/{id}/` - Update event
- `DELETE /events/{id}/` - Delete event
- `POST /events/{id}/register/` - Register for event
- `POST /events/{id}/unregister/` - Unregister from event
- `GET /events/{id}/participants/` - Get event participants
- `GET /events/{id}/report/` - Get event report
- `GET /events/my-events/` - Get user's created events
- `GET /events/registered-events/` - Get user's registered events

#### Notifications
- `GET /notifications/` - List user notifications
- `GET /notifications/{id}/` - Get notification details
- `PATCH /notifications/{id}/` - Update notification (mark as read)
- `POST /notifications/{id}/mark-as-read/` - Mark notification as read
- `POST /notifications/mark-all-as-read/` - Mark all notifications as read
- `GET /notifications/unread-count/` - Get unread count
- `GET /notifications/recent/` - Get recent notifications

## Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test Files
```bash
pytest tests/test_users.py
pytest tests/test_events.py
pytest tests/test_notifications.py
```

### Run with Coverage
```bash
pytest --cov=. --cov-report=html
```

### Test Categories
1. **User Tests**: User model, authentication, profile management
2. **Event Tests**: Event CRUD, participant management, validation
3. **Notification Tests**: Notification system, async tasks
4. **Integration Tests**: End-to-end API functionality

## Project Structure

```
event-management-system/
├── event_management/          # Main Django project
│   ├── settings.py           # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── celery.py            # Celery configuration
│   └── wsgi.py              # WSGI configuration
├── users/                    # User management app
│   ├── models.py            # Custom User model
│   ├── serializers.py       # User serializers
│   ├── views.py             # User views
│   ├── urls.py              # User URLs
│   └── admin.py             # Admin interface
├── events/                   # Event management app
│   ├── models.py            # Event and EventParticipant models
│   ├── serializers.py       # Event serializers
│   ├── views.py             # Event views
│   ├── urls.py              # Event URLs
│   └── admin.py             # Admin interface
├── notifications/            # Notification system app
│   ├── models.py            # Notification model
│   ├── serializers.py       # Notification serializers
│   ├── views.py             # Notification views
│   ├── tasks.py             # Celery tasks
│   ├── urls.py              # Notification URLs
│   └── admin.py             # Admin interface
├── tests/                    # Test suite
│   ├── test_users.py        # User tests
│   ├── test_events.py       # Event tests
│   └── test_notifications.py # Notification tests
├── requirements.txt          # Python dependencies
├── manage.py                # Django management script
├── pytest.ini              # Pytest configuration
├── env.example              # Environment variables example
└── README.md               # This file
```

## Security Features

### Authentication & Authorization
- Custom User model with email as primary identifier
- Password validation and secure storage
- Session and token authentication
- Permission-based access control

### Data Protection
- Input validation and sanitization
- SQL injection prevention through ORM
- XSS protection through Django's built-in security
- CSRF protection enabled

### API Security
- Rate limiting (can be configured)
- Secure headers
- CORS configuration
- Environment-based security settings

## Performance & Scalability

### Database Optimization
- Proper indexing on frequently queried fields
- Efficient query patterns with select_related and prefetch_related
- Database connection pooling support

### Asynchronous Processing
- Celery for background task processing
- Redis as message broker
- Non-blocking notification delivery
- Scalable worker architecture

### Caching Strategy
- Redis for session storage
- Query result caching capabilities
- Static file caching

## Deployment

### Production Checklist
1. Set `DEBUG=False` in settings
2. Configure proper `SECRET_KEY`
3. Set up production database
4. Configure email settings
5. Set up Redis for Celery
6. Configure static file serving
7. Set up monitoring and logging

### Docker Support
The project can be containerized using Docker and Docker Compose for easy deployment.

### Environment Variables
All sensitive configuration is externalized through environment variables.

## Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Write comprehensive tests
- Update documentation as needed

## License

This project is licensed under the MIT License.

## Support

For questions or support, please contact the development team or create an issue in the repository.

## Changelog

### Version 1.0.0
- Initial release
- Complete CRUD functionality for users and events
- Notification system with async processing
- Comprehensive test suite
- API documentation
- Security features implemented 