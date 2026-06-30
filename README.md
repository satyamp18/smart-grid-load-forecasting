# Smart Grid Operations Center

Welcome to the **Smart Grid Operations Center** project. This system is designed for high-frequency consumption monitoring, overload warning generation, real-time analytics aggregation, and background scheduling.

---

## 🏗️ System Architecture

The application is structured into two main components:
1. **`smartgrid` (Core Services & API):** Relational database-backed services, FastAPI routes, and SQLAlchemy models developed to manage Zones, Smart Meters, and Meter Readings.
2. **`app` (Analytics, Caching & Task Scheduler):** Member 3 modules integrating Redis for in-memory caching and real-time state hashes, and Celery for automated background workers and Beat periodic tasks.

---

## 📂 Project Structure

```text
smart-grid-load-forecasting/
├── app/
│   ├── alerts.py            # CSV Alert triggers & warning logging (Day 3)
│   ├── analytics.py         # CSV Analytics reporting with Redis Cache-Aside (Day 4)
│   ├── redis_client.py      # Reusable Redis connection pool & data utilities (Day 4)
│   ├── celery_app.py        # Celery broker/backend configuration and Beat scheduler (Day 6-7)
│   ├── tasks.py             # Celery background task definitions (Day 6-7)
│   ├── test_redis.py        # Verification script for Redis functions
│   └── test_celery.py       # Asynchronous task dispatch validation script
├── smartgrid/
│   ├── api/v1/              # FastAPI Routers for Zones, Meters, and Analytics
│   ├── core/                # System settings and logger setup
│   ├── db/                  # SQLAlchemy connection session configurations
│   ├── models/              # DB schemas (Zone, SmartMeter, MeterReading, etc.)
│   ├── repositories/        # Database CRUD handlers
│   ├── services/            # Business services (LoadService, AlertService)
│   └── utils/
│       └── seed_data.py     # Database seeder script
├── data/
│   ├── alerts.log           # Persisted logs of triggered CSV overload alerts
│   └── sample_meter_data.csv# Input CSV dataset for smart meter data
├── requirements.txt         # Unified python packages requirements
├── alembic.ini              # Alembic database migration settings
├── test.db                  # Local SQLite database file
└── .env                     # System environment settings
```

---

## 🛠️ Setup & Quick Start

### 1. Start Redis Server
Ensure that Redis is running locally on `localhost:6379`. If you compiled the server from source, start it via:
```bash
./redis-stable/src/redis-server --daemonize yes
```

### 2. Configure Environment `.env`
Create or edit `.env` in the root folder to point to your target database. For local SQLite execution:
```env
DATABASE_URL=sqlite:///test.db
```

### 3. Initialize & Seed Database
Build the database tables and populate them with test zones and meters:
```bash
# 1. Create SQL database tables
PYTHONPATH=. DATABASE_URL=sqlite:///test.db python3 -c "from smartgrid.db.base import Base; from smartgrid.db.session import engine; import smartgrid.models; Base.metadata.create_all(bind=engine)"

# 2. Seed testing data
PYTHONPATH=. DATABASE_URL=sqlite:///test.db python3 smartgrid/utils/seed_data.py
```

### 4. Run the Celery Worker & Beat Scheduler
Start Celery in beat-scheduler mode in a separate terminal:
```bash
PYTHONPATH=. celery -A app.celery_app worker --beat --loglevel=info
```

### 5. Run the FastAPI Web Application
Start the FastAPI server:
```bash
PYTHONPATH=. uvicorn smartgrid.main:app --reload
```
You can view the interactive documentation at `http://127.0.0.1:8000/docs`.

---

## 🧪 Testing Verification

*   **Test Redis Caching & Hashes:**
    ```bash
    python3 app/test_redis.py
    ```
*   **Test Asynchronous Tasks Dispatch:**
    ```bash
    python3 app/test_celery.py
    ```
*   **Observe Caching Speedup:**
    ```bash
    python3 app/analytics.py
    ```
    *(Run twice: the first is a Cache Miss; the second is a Cache Hit, loading directly from Redis).*

*   **Test Asynchronous API Endpoints (FastAPI + Celery):**
    Ensure the FastAPI application and Celery worker are running, then run:
    ```bash
    # Trigger load report calculation asynchronously for Zone 1:
    curl -X POST http://127.0.0.1:8000/api/v1/load-reports/trigger/1

    # Trigger overload check/alerts asynchronously for Zone 1:
    curl -X POST http://127.0.0.1:8000/api/v1/alerts/check/1
    ```

---

## ⚡ Celery Integration & Background Schedules

1. **Dynamic Configuration:** Broker and backend connections are configured dynamically via `REDIS_URL` specified in `.env` (defaulting to local Redis `redis://localhost:6379/0`), parsed via Pydantic `Settings`.
2. **Circular Dependency Avoidance:** To support clean Python architecture, `LoadService` and `AlertService` perform local imports inside their async methods (`generate_load_report_async` and `check_overload_async`) to dispatch tasks without introducing import loops with `app.tasks`.
3. **Independent Periodic Schedules (Celery Beat):** Periodic tasks are split into two decoupled processes running every **2 minutes (120 seconds)**:
   - `generate-load-reports-every-2-minutes`: Executes `generate_load_reports_all_zones_task` to compute and record loads for all registered zones.
   - `check-alerts-every-2-minutes`: Executes `check_overload_all_zones_task` to run utilization safety margin checks (alerts triggered if >90% capacity).
4. **Task Isolation:** Worker logs provide clear trace logs indicating whether a zone operates within limit capacity or flags a critical overload alert.

