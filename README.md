# ai-fraud-detection-biometrics
Great 👍 I’ll create a **GitHub-ready README.md** for your project. You can just copy-paste this into your repo’s `README.md` file.

---

# 📌 AI Fraud Detection via Behavioral Biometrics

## 📖 Project Overview

This project demonstrates an **AI-powered fraud detection system for online banking**.
It uses **behavioral biometrics** such as **keystroke dynamics, mouse movement patterns, and interaction timings** to detect suspicious login/payment attempts.

✅ Features:

* Collects **keystrokes, mouse paths, and gestures** via frontend (mock banking UI)
* **FastAPI backend** for data ingestion & scoring
* **ML models** (One-Class SVM, Isolation Forest, Autoencoder) to detect anomalies
* **Risk policy engine** with thresholds & step-up authentication (e.g., OTP)
* **Dashboard (Streamlit/Plotly)** for monitoring transactions & model decisions

---

## 🏗️ Architecture Diagram

![Architecture](docs/architecture.png)
*(Upload your diagram image into a folder `docs/` in this repo, then rename it to `architecture.png`)*

---

## 📂 Repository Structure

```
ai-fraud-detection-biometrics/
│── backend/         # FastAPI app (ingestion API, scoring logic, models)
│── frontend/        # Mock banking UI (login & payment pages, JS data collector)
│── dashboard/       # Streamlit dashboard (analytics, monitoring, audit logs)
│── data/            # Datasets (synthetic keystrokes, mouse paths, CSVs)
│── demo/            # Demo scripts, run instructions
│── docs/            # Documentation + architecture diagrams
│── README.md        # Project description (this file)
```

---

## ⚙️ Tech Stack

* **Frontend:** HTML/JS (keystroke & mouse capture)
* **Backend:** Python, FastAPI, scikit-learn, TensorFlow/PyTorch
* **Dashboard:** Streamlit / Plotly
* **Database:** SQLite/Postgres
* **Deployment:** Local demo (can be extended to Docker/Kubernetes)

---

## 🚀 Quick Start

1. Clone repo:

   ```bash
   git clone https://github.com/your-username/ai-fraud-detection-biometrics.git
   cd ai-fraud-detection-biometrics
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run backend:

   ```bash
   uvicorn backend.main:app --reload
   ```
4. Run dashboard:

   ```bash
   streamlit run dashboard/app.py
   ```
5. Open frontend:

   * `http://127.0.0.1:8000/docs` → API
   * `http://127.0.0.1:8501` → Dashboard
   * `frontend/index.html` → Mock banking UI

---

## 📊 Workflow

1. User interacts with **banking UI** → keystrokes & mouse gestures collected
2. Data sent as **JSON → FastAPI backend**
3. Backend extracts **features (dwell time, flight time, velocity, hesitation)**
4. ML models generate **risk score**
5. **Risk policy layer** decides: *Approve / Flag / Step-Up Auth*
6. Dashboard shows **real-time results & logs**

---

## 🎯 Outcomes

* Demonstrates a **practical cybersecurity project** for students
* Shows how **AI + biometrics** can fight fraud in real-world banking
* Includes **live monitoring dashboard** for transparency

---

## 🧑‍💻 Author

   
  LITHIN KUMAR M– Final Year Computer Science Student
📧 Contact:(mailto:lluckylithin@gmail.com)


