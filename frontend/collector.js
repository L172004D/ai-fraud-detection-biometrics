// frontend/collector.js
const events = [];
let lastMoveTs = 0;

document.addEventListener('keydown', e => {
  events.push({t: performance.now(), type: 'down', k: e.key});
});

document.addEventListener('keyup', e => {
  events.push({t: performance.now(), type: 'up', k: e.key});
});

document.addEventListener('mousemove', e => {
  const now = performance.now();
  if (now - lastMoveTs > 30) {
    events.push({t: now, type: 'move', x: e.clientX, y: e.clientY});
    lastMoveTs = now;
  }
});

async function submitBehavior(user_id) {
  const payload = { user_id, events };
  try {
    const res = await fetch('http://127.0.0.1:8000/risk_score', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    return await res.json();
  } catch(err) {
    return {error: 'Could not reach backend. Is uvicorn running?', detail: err.toString()};
  }
}

window.behavior = { events, submitBehavior };
