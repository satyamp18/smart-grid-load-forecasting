from fastapi import FastAPI

app = FastAPI(
    title="Smart Grid Load Balancing API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Smart Grid API Running"}