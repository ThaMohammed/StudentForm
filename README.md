# Student Registration System

A web application for managing student registrations for software training classes.

## Features

- User authentication and authorization.
- Student registration form.
- Dashboard for viewing registrations.
- Admin features:
  - User management
  - Export registrations to CSV
  - View all registrations
- API endpoints for all operations

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- Node.js and npm (for frontend)

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a PostgreSQL database:
```sql
CREATE DATABASE student_registration;
```

4. Create a `.env` file in the backend directory with:
```
DATABASE_URL=postgresql://postgres:postgres@localhost/student_registration
SECRET_KEY=your-super-secret-key-here
```

5. Run the backend server:
```bash
cd backend
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- POST `/token` - Login and get access token

### Users
- POST `/users/` - Create new user (admin only)

### Registrations
- POST `/registrations/` - Create new registration
- GET `/registrations/` - List all registrations
- GET `/registrations/{id}` - Get specific registration
- PUT `/registrations/{id}` - Update registration
- DELETE `/registrations/{id}` - Delete registration
- GET `/export/registrations` - Export all registrations to CSV (admin only)

## Security

- All endpoints except `/token` require authentication
- Passwords are hashed using bcrypt
- JWT tokens are used for authentication
- Admin-only endpoints are protected
- Users can only access their own registrations 
