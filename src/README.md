# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities
- Role-based authorization for management operations

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister from an activity                                     |
| POST   | `/activities`                                                     | Create activity (organizer/admin only)                             |
| PATCH  | `/activities/{activity_name}`                                     | Update activity (organizer/admin only)                             |
| DELETE | `/activities/{activity_name}`                                     | Delete activity (organizer/admin only)                             |

## Access Rules

The API uses a lightweight mock auth header, `X-User-Role`, with these valid values:

- `student`
- `organizer`
- `admin`

Rules:

- If `X-User-Role` is omitted, the API treats the request as `student`.
- `student` can list activities and sign up/unregister.
- `organizer` and `admin` can create, update, and delete activities.
- Invalid role values return `401`.
- Authenticated roles without sufficient permissions return `403`.

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
