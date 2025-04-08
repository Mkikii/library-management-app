# Library Management System

A modern web application for library management built with Flask and Vue.js, deployed on Heroku.

## Tech Stack

- **Backend**: Flask 2.0.1, Python 3.9+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Frontend**: Vue.js 3, Bootstrap 5
- **Testing**: pytest with coverage
- **Deployment**: Heroku with Gunicorn

## Features

- Book Management (CRUD, search, stock tracking)
- Member Management (registration, debt tracking)
- Transaction System (issue/return books, automatic fee calculation)
- Real-time Dashboard with Statistics
- RESTful API Integration
- Automated Testing Suite

## Local Development Setup

1. Clone and install dependencies:
```bash
git clone https://github.com/yourusername/library-management-app.git
cd library-management-app
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

2. Set up PostgreSQL database:
```bash
createdb library_db
```

3. Configure environment variables in `.env`:

## Testing

Run the test suite:

```bash
pytest tests/ --cov=app
```

The application includes:
- Unit tests for models
- Integration tests for routes
- Coverage reporting

## Vue.js Integration

The frontend uses Vue.js 3 for reactive components:
- Book management interface
- Real-time search
- Transaction management

## API Documentation

### Books API
- GET /api/books - List all books
- POST /api/books - Create new book
- PUT /api/books/<id> - Update book
- DELETE /api/books/<id> - Delete book

### Members API
- GET /api/members - List all members
- POST /api/members - Create new member
- PUT /api/members/<id> - Update member

### Transactions API
- POST /api/transactions/issue - Issue book
- POST /api/transactions/return - Return book
- GET /api/transactions/history/<member_id> - Get member history

## Deployment

### Heroku Deployment
1. Install Heroku CLI
2. Login to Heroku
3. Create new app
4. Push to Heroku:
```bash
heroku create
git push heroku main
```
