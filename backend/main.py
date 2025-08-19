# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import csv, os, time, math
import numpy as np

app = FastAPI(title="Behavioral Biometrics Fraud Demo")

SCORES_CSV = os.path.join(os.path.dirname(__file__), "scores.csv")

# ensure CSV exists with header
if not os.path.exists(SCORES_CSV):
    with open(SCORES_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ts_ms", "user_id", "risk_pct", "decision",
                         "dwell_mean", "flight_mean", "error_rate", "mouse_speed_p95", "gesture_entropy"])

class Event(BaseModel):
    t: float
    type: str
    k: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None

class Session(BaseModel):
    user_id: str
    events: List[Event]

def p95(arr):
    if len(arr) == 0:
        return 0.0
    return float(np.percentile(arr, 95))

def gesture_entropy(angles):
    if len(angles) == 0:
        return 0.0
    hist, _ = np.histogram(angles, bins=12)
    p = hist / (hist.sum() + 1e-9)
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())

def extract_features(events):
    downs = {}
    dwell = []
    flight = []
    last_up = None
    errs = 0
    total_keys = 0

    xs, ys, ts = [], [], []
    for e in events:
        et = e["type"]
        t = float(e.get("t", 0.0))
        if et == "down":
            total_keys += 1
            k = e.get("k")
            if k in downs:
                errs += 1
            downs[k] = t
            if last_up is not None:
                flight.append(max(0.0, t - last_up))
                last_up = None
        elif et == "up":
            k = e.get("k")
            if k in downs:
                dwell.append(max(0.0, t - downs.pop(k)))
                last_up = t
        elif et == "move":
            xs.append(float(e.get("x", 0.0)))
            ys.append(float(e.get("y", 0.0)))
            ts.append(t)

    xs = np.array(xs) if len(xs) > 0 else np.array([])
    ys = np.array(ys) if len(ys) > 0 else np.array([])
    ts = np.array(ts) if len(ts) > 0 else np.array([])

    speeds = []
    angles = np.array([])
    if len(ts) >= 2:
        dt = np.diff(ts) / 1000.0
        dt[dt == 0] = 1e-6
        dx = np.diff(xs)
        dy = np.diff(ys)
        speed = np.sqrt(dx*dx + dy*dy) / dt
        speeds = speed.tolist()
        angles = np.arctan2(dy, dx)

    dwell_mean = float(np.mean(dwell)) if dwell else 0.0
    flight_mean = float(np.mean(flight)) if flight else 0.0
    error_rate = float(errs / max(1, total_keys))
    mouse_speed_p95 = p95(speeds)
    gest_entropy = gesture_entropy(angles)

    return {
        "dwell_mean": dwell_mean,
        "flight_mean": flight_mean,
        "error_rate": error_rate,
        "mouse_speed_p95": mouse_speed_p95,
        "gesture_entropy": gest_entropy
    }

def compute_risk(feat):
    # very simple heuristic baseline: normalize each feature roughly,
    # then make a weighted sum -> risk percent
    d = feat["dwell_mean"] / 300.0
    f = feat["flight_mean"] / 300.0
    e = feat["error_rate"] * 5.0
    m = feat["mouse_speed_p95"] / 800.0
    g = feat["gesture_entropy"] / 5.0
    score = (0.35*d + 0.25*f + 0.15*e + 0.15*m + 0.10*g)
    # clamp 0..1
    score = max(0.0, min(1.0, score))
    return float(score * 100.0)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/risk_score")
def risk_score(session: Session):
    evs = [e.dict() for e in session.events]
    feats = extract_features(evs)
    risk_pct = compute_risk(feats)
    if risk_pct < 35:
        decision = "ALLOW"
    elif risk_pct < 70:
        decision = "STEP_UP"
    else:
        decision = "BLOCK"

    # append to CSV
    with open(SCORES_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([int(time.time()*1000), session.user_id, round(risk_pct,2),
                         decision, feats["dwell_mean"], feats["flight_mean"],
                         feats["error_rate"], feats["mouse_speed_p95"],
                         feats["gesture_entropy"]])

    return {"risk_pct": round(risk_pct,2), "decision": decision, "features": feats}
 
