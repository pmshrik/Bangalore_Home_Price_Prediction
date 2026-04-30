# Bangalore Home Price Prediction

## Project structure

- `frontend/`: static UI (HTML/CSS/JS)
- `backend/`: Flask API + prediction logic
  - `backend/artifacts/`: trained model + `columns.json`
  - `backend/notebooks/`: training notebook(s)
  - `backend/config/`: config files
- `db/`: dataset(s)

## Run backend

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

From the repo root:

```bash
python -m backend.server
```

Or from inside `backend/`:

```bash
python server.py
```