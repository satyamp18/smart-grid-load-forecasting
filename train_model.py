import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Sample training data
data = pd.DataFrame({
    "temperature": [20, 25, 30, 35, 40, 22, 28, 33],
    "hour": [8, 10, 12, 14, 16, 18, 20, 22],
    "load": [45, 55, 68, 82, 95, 60, 72, 85]
})

X = data[["temperature", "hour"]]
y = data["load"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "smartgrid_model.pkl")

print("✅ Model trained and saved!")
