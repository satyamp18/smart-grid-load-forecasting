from smartgrid.services.model import predict_load
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
app = FastAPI(
    title="Smart Grid Operations Center",
    version="1.0.0"
)

# CORS (frontend connect ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model (IMPORTANT)
class ForecastRequest(BaseModel):
    temperature: float
    hour: int

# Root API
@app.get("/")
def home():
    return {"message": "Smart Grid API is running 🚀"}

# Health check API
@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/forecast")
def forecast(req: ForecastRequest):
    prediction = predict_load(req.temperature, req.hour)

    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO forecasts
        (temperature, hour, predicted_load)
        VALUES (?, ?, ?)
        """,
        (req.temperature, req.hour, prediction)
    )

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "temperature": req.temperature,
        "hour": req.hour,
        "predicted_load": round(prediction, 2),
        "unit": "MW"
    }
# Forecast API
@app.get("/forecasts")
def get_forecasts():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, temperature, hour, predicted_load FROM forecasts"
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "temperature": row[1],
            "hour": row[2],
            "predicted_load": round(row[3], 2)
        }
        for row in rows
    ]
