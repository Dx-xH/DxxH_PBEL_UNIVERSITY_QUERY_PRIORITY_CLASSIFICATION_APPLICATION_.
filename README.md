# 🎓 University Query Priority Classifier

> An AI-powered triage system that classifies student support queries by urgency — helping university staff respond to what matters most, first.

---

## 📌 Overview

Students submit hundreds of queries daily to university departments — scholarship issues, registration deadlines, financial holds, housing concerns, and more. Not all of these are equally urgent. This project uses a trained machine learning pipeline to automatically classify each incoming query as **High**, **Medium**, or **Low** priority based on:

- The **content** of the student's message
- The **department** it's addressed to
- The **number of days remaining** until a deadline

The result is a fast, consistent, and explainable triage layer that plugs directly into your support workflow.

---

## 🗂️ Project Structure

```
.
├── main.py            # FastAPI backend — prediction API
├── pipeline.pkl       # Trained scikit-learn ML pipeline (model + preprocessor)
├── template.html      # Standalone frontend UI (no build step required)
├── requirements.txt   # Python dependencies
└── Dockerfile         # Container configuration for deployment
```

---

## ⚙️ How It Works

### Backend — `main.py`

Built with **FastAPI**, the backend exposes a single prediction endpoint:

- **`GET /`** — Health check; confirms the API is running.
- **`POST /predict`** — Accepts a JSON payload and returns a priority classification.

**Request body:**
```json
{
  "Student_Query": "I haven't received my scholarship letter and the deadline is in 2 days.",
  "Department": "Finance",
  "Days_To_Deadline": 2
}
```

**Response:**
```json
{
  "Student_Query": "...",
  "Department": "Finance",
  "Days_To_Deadline": 2,
  "priority": "High",
  "confidence": 0.94
}
```

The model is loaded from `pipeline.pkl` at startup using `joblib`. The pipeline handles all preprocessing and inference internally, so raw inputs can be passed directly.

### ML Pipeline — `pipeline.pkl`

A pre-trained **scikit-learn pipeline** that encapsulates:
- Text feature extraction from the student query
- Encoding of the department field
- Use of `Days_To_Deadline` as a numerical feature
- A classification model that predicts priority level and (where supported) outputs confidence scores via `predict_proba`

### Frontend — `template.html`

A fully self-contained, single-file frontend UI with no build step or framework dependencies. Open it directly in any browser.

**Features:**
- 🎨 Dark-mode UI with animated glowing orbs and a noise texture overlay
- 📝 Text area for entering the student query
- 🏛️ Department selector (10 common university departments pre-loaded)
- 🎚️ Interactive slider for days-to-deadline (0–60)
- 🔗 Configurable API URL bar with a live connection status indicator
- 📊 Result card showing priority level with color coding (🔴 High / 🟠 Medium / 🟢 Low)
- 🔵 Animated confidence ring displaying model certainty as a percentage
- `{ }` Raw JSON toggle for inspecting the full API response
- 🕘 Session query history (last 20 queries) stored in `localStorage`, with click-to-refill
- ⌨️ `Ctrl + Enter` keyboard shortcut to submit
- 📱 Fully responsive for mobile screens

---

## 🚀 Getting Started

### Option 1 — Run Locally (Python)

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Start the API server:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**3. Open the frontend:**

Simply open `template.html` in your browser. The API URL is pre-set to `http://localhost:8000/predict`.

**4. Verify the API is live:**
```bash
curl http://localhost:8000/
# {"message":"University Query Priority API is running 🚀"}
```

---

### Option 2 — Run with Docker

**1. Build the image:**
```bash
docker build -t query-priority-api .
```

**2. Run the container:**
```bash
docker run -p 8000:8000 query-priority-api
```

**3. Open `template.html`** in your browser — the default API URL will work out of the box.

---

## 📡 API Reference

### `POST /predict`

| Field | Type | Required | Description |
|---|---|---|---|
| `Student_Query` | `string` | ✅ | The student's message or query text |
| `Department` | `string` | ✅ | The university department being contacted |
| `Days_To_Deadline` | `integer` | ✅ | Days remaining until a relevant deadline (≥ 0) |

**Validation rules:**
- `Student_Query` cannot be blank
- `Days_To_Deadline` cannot be negative

**Error responses:**
- `400` — Invalid input (empty query or negative days)
- `500` — Internal model inference error

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `fastapi` | API framework |
| `uvicorn` | ASGI server |
| `scikit-learn==1.6.1` | ML pipeline & model (pinned for compatibility with `pipeline.pkl`) |
| `pandas` | DataFrame construction for model input |
| `joblib` | Model deserialization |
| `tensorflow` / `keras` | Deep learning support (if used in pipeline) |
| `numpy` | Numerical operations |

> ⚠️ **Important:** `scikit-learn` is pinned to `1.6.1`. Changing this version may cause `pipeline.pkl` to fail to load due to serialization incompatibilities.

---

## 🐳 Docker Details

The `Dockerfile` uses `python:3.10-slim` as its base image for a minimal footprint. Key design decisions:

- `requirements.txt` is copied and installed **before** the rest of the source code, so Docker can cache the dependency layer and speed up rebuilds when only code changes.
- `PYTHONUNBUFFERED=1` ensures logs appear in real time in the container output.
- The app is served on port `8000` via `uvicorn`.

---

## 🔒 Security Notes

- CORS is currently set to `allow_origins=["*"]`. **This should be restricted to known frontend origins in production.**
- Consider adding API key authentication before exposing this service publicly.
- The `pipeline.pkl` file is a serialized Python object. Only use model files from trusted sources, as malicious pickle files can execute arbitrary code on load.

---

## 🛠️ Customization

**Adding more departments to the frontend:**
Edit the `<select id="deptInput">` dropdown in `template.html` and add new `<option>` elements.

**Retraining the model:**
Replace `pipeline.pkl` with a new pipeline trained using the same input feature names (`Student_Query`, `Department`, `Days_To_Deadline`). Ensure you use `scikit-learn==1.6.1` during training to maintain compatibility.

**Changing the API port:**
Update the `uvicorn` command in the `Dockerfile` CMD and the default value of the API URL input in `template.html`.

---

## 📄 License

This project is intended for educational purposes only.


This project is open for academic and educational use.
