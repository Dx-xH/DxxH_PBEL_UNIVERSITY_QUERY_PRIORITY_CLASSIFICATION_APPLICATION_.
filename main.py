from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(
    title="University Query Priority Prediction API",
    version="1.0"
)

# -----------------------------
# Load Model & Preprocessing
# -----------------------------
try:
     model = joblib.load("pipeline.pkl")

except Exception as e:
    raise RuntimeError(f"Error loading model: {e}")


# -----------------------------
# Input Schema
# -----------------------------
class QueryInput(BaseModel):
    Student_Query: str
    Department: str
    Days_To_Deadline: int


@app.get("/")
def home():
    return {"message": "University Query Priority API is running 🚀"}


@app.post("/predict")
def predict(data: QueryInput):

    if not data.Student_Query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    if data.Days_To_Deadline < 0:
        raise HTTPException(status_code=400, detail="Days cannot be negative")

    try:
        # Create DataFrame exactly as training
        input_df = pd.DataFrame({
            "Student_Query": [data.Student_Query],
            "Department": [data.Department],
            "Days_To_Deadline": [data.Days_To_Deadline]
        })

        prediction = model.predict(input_df)[0]

        confidence = None
        if hasattr(model, "predict_proba"):
            confidence = float(model.predict_proba(input_df).max())

        return {
            "Student_Query": data.Student_Query,
            "Department": data.Department,
            "Days_To_Deadline": data.Days_To_Deadline,
            "priority": prediction,
            "confidence": confidence
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))