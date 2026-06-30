import joblib

model = joblib.load("smartgrid_model.pkl")

def predict_load(temp, hour):
    prediction = model.predict([[temp, hour]])
    return float(prediction[0])
