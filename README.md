# DxxH_PBEL_UNIVERSITY_QUERY_PRIORITY_CLASSIFICATION_APPLICATION_.

# 🎓 University Query Priority Classifier

A machine learning-powered REST API that automatically classifies incoming student queries by priority level — helping university staff triage and respond to the most urgent issues first.

---

## 📌 Overview

University support teams receive a high volume of student queries daily across multiple departments. Manually sorting these by urgency is time-consuming and error-prone. This project solves that by training an ML pipeline that takes a student's query text, their department, and their deadline proximity — and predicts a **priority label** (e.g., High / Medium / Low) in real time.

The model is served via a **FastAPI** REST API, containerized with **Docker** for easy deployment anywhere.

---

## 🧠 How It Works

The core of the project is a **scikit-learn ML pipeline** (`pipeline.pkl`) that combines:

- **TF-IDF Vectorizer** — converts raw student query text into numerical features
- **One-Hot Encoder** — encodes the `Department` categorical field
- **Standard Scaler** — normalizes the `Days_To_Deadline` numerical feature
- **Classifier** — trained on labeled university query data to predict priority

All preprocessing and prediction happen in a single pipeline call, ensuring consistency between training and inference.

---

## 📥 Input

The API accepts a JSON body with three fields:

| Field | Type | Description |
|---|---|---|
| `Student_Query` | `string` | The text of the student's question or request |
| `Department` | `string` | The department the query is directed to (e.g., "Finance", "Admissions") |
| `Days_To_Deadline` | `int` | Number of days remaining until a relevant deadline |

---

## 📤 Output

```json
{
  "Student_Query": "I haven't received my scholarship letter yet",
  "Department": "Finance",
  "Days_To_Deadline": 3,
  "priority": "High",
  "confidence": 0.91
}
```

---

## 🚀 Running the Project

### Option 1: Docker (Recommended)

```bash
# Build the image
docker build -t university-query-api .

# Run the container
docker run -p 8000:8000 university-query-api
```

The API will be available at `http://localhost:8000`

### Option 2: Local (Python)

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🔌 API Endpoints

### `GET /`
Health check — confirms the API is running.

### `POST /predict`
Classify a student query by priority.

**Example request:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Student_Query": "My exam timetable has an overlap",
    "Department": "Registrar",
    "Days_To_Deadline": 5
  }'
```

You can also explore and test all endpoints via the **interactive Swagger UI** at:
```
http://localhost:8000/docs
```

---

## 🗂️ Project Structure

```
├── main.py            # FastAPI app — endpoints and prediction logic
├── pipeline.pkl       # Trained scikit-learn ML pipeline (preprocessing + model)
├── requirements.txt   # Python dependencies
└── Dockerfile         # Container setup for deployment
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10 | Core language |
| FastAPI | REST API framework |
| scikit-learn | ML pipeline (TF-IDF, OHE, Scaler, Classifier) |
| pandas | Input data handling |
| joblib | Model serialization |
| Docker | Containerization & deployment |
| Uvicorn | ASGI server |

---

## ⚙️ Requirements

See `requirements.txt`. Key dependencies:

```
fastapi
uvicorn
scikit-learn==1.6.1
pandas
joblib
numpy
```

> ⚠️ **Note:** The `pipeline.pkl` was trained with `scikit-learn==1.6.1`. Use the same version to avoid deserialization warnings or errors.

---

## 📄 License

This project is open for academic and educational use.
