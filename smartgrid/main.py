from smartgrid.services.model import predict_load
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# Forecast API
@app.post("/forecast")
def forecast(req: ForecastRequest):
    prediction = predict_load(req.temperature, req.hour)

    return {
    "status": "success",
    "temperature": req.temperature,
    "hour": req.hour,
    "predicted_load": round(prediction, 2),
    "unit": "MW"
}
