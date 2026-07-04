# Smart Grid Load Balancing & Forecasting API

A backend system for monitoring and managing smart grid operations. The project provides APIs to manage grid zones, smart meters, meter readings, load reports, and alerts while offering a dashboard for monitoring the overall system status. The architecture is designed to support future integration with machine learning models for load forecasting and real-time monitoring.

---

## Features

- Zone Management
- Smart Meter Management
- Meter Reading Management
- Load Analytics
- Alert Generation
- Load Report Generation
- Dashboard Summary
- Dashboard Health Monitoring
- RESTful APIs using FastAPI
- PostgreSQL Database Integration
- Swagger API Documentation

---

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic

### Database
- PostgreSQL

### API Testing
- Swagger UI
- Postman

### Frontend (In Progress)
- React
- Vite
- Tailwind CSS
- Axios

### Planned Integrations
- Machine Learning
- Celery
- WebSockets

---

## Project Structure

```
smartgrid/
│
├── api/
├── core/
├── db/
├── models/
├── repositories/
├── schemas/
├── services/
├── tasks/
├── utils/
├── websocket/
└── main.py
```

---

## Database Design

The project is built around the following entities:

- Zone
- Smart Meter
- Meter Reading
- Alert
- Load Report

The database is managed using PostgreSQL with SQLAlchemy ORM and Alembic migrations.

---

## API Modules

### Zone

- Create Zone
- Get All Zones
- Get Zone
- Update Zone
- Delete Zone

### Smart Meter

- Register Meter
- Get Meters
- Delete Meter

### Meter Reading

- Add Reading
- View Readings
- Delete Reading


### Analytics

- Zone-wise Load Analysis
- Grid Statistics

### Alert

- Generate Alerts
- View Alerts

### Load Report

- Generate Reports
- View Reports

### Dashboard

- Dashboard Summary
- System Health

---

## Project Workflow

```
Smart Meter
      │
      ▼
Meter Reading API
      │
      ▼
Database
      │
      ▼
Analytics
      │
      ▼
Alert Generation
      │
      ▼
Load Reports
      │
      ▼
Dashboard
```

---

## Current Status

| Module | Status |
|----------|--------|
| Database Design | ✅ |
| Models | ✅ |
| Repository Layer | ✅ |
| Service Layer | ✅ |
| CRUD APIs | ✅ |
| Analytics | ✅ |
| Alerts | ✅ |
| Load Reports | ✅ |
| Dashboard | ✅ |
| API Testing | ✅ |
| Frontend | 🚧 |
| Machine Learning | 🚧 |

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/smart-grid-load-forecasting.git
```

Move to the project directory

```bash
cd smart-grid-load-forecasting
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure the database

```
DATABASE_URL=postgresql://username:password@localhost:5432/smartgrid
```

Run migrations

```bash
alembic upgrade head
```

Start the server

```bash
uvicorn smartgrid.main:app --reload
```

---

## API Documentation

After running the server

Swagger

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## Future Improvements

- Machine Learning based Load Forecasting
- Live Dashboard using WebSockets
- Background Task Processing using Celery
- Authentication and Role-Based Access
- Docker Deployment
- Cloud Deployment

---

## Contributors

- Backend Development
- Database Design
- Frontend Development
- Machine Learning
- API Integration

---

## License

This project was developed as part of the **Bharatiya Antariksh Hackathon (BAH) 2026**.