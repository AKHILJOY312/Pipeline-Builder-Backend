# Pipeline Processing Engine (Backend)

FastAPI backend service for parsing pipeline graph payloads and checking whether the graph is a DAG (Directed Acyclic Graph).

## Tech Stack

- Python 3.14+
- FastAPI
- Uvicorn
- Pydantic

## Project Structure

```text
backend/
├─ app/
│  ├─ api/routes/pipelines.py      # Pipeline API endpoint
│  ├─ schemas/pipeline.py          # Request schemas
│  ├─ services/pipeline_validator.py # DAG validation logic
│  ├─ core/errors.py               # Global/custom exception handlers
│  └─ main.py                      # FastAPI app setup
├─ main.py                         # ASGI entrypoint (exports app)
├─ pyproject.toml
└─ README.md
```

## Setup

### Option 1: Using `uv` (recommended)

```bash
uv sync
```

### Option 2: Using `pip`

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install fastapi uvicorn python-multipart
```

## Run the Server

From the `backend` directory:

```bash
uv run uvicorn main:app --reload
```

Or with plain Python environment:

```bash
uvicorn main:app --reload
```

Server default: `http://127.0.0.1:8000`

## API Endpoints

### `GET /`

Health-style ping endpoint.

Example response:

```json
{ "Ping": "Pong" }
```

### `POST /pipelines/parse`

Accepts a pipeline graph and returns node/edge counts plus whether it is a DAG.

Request body:

```json
{
  "nodes": [
    { "id": "A", "type": "source" },
    { "id": "B", "type": "processor" },
    { "id": "C", "type": "sink" }
  ],
  "edges": [
    { "id": "e1", "source": "A", "target": "B" },
    { "id": "e2", "source": "B", "target": "C" }
  ]
}
```

Success response:

```json
{
  "success": true,
  "num_nodes": 3,
  "num_edges": 2,
  "is_dag": true
}
```

Validation notes:

- `nodes` must contain at least one item.
- Each node requires: `id`, `type`.
- Each edge requires: `id`, `source`, `target`.

## Error Handling

Standardized JSON errors are returned for:

- Validation errors (`422`)
- HTTP errors, including route-not-found (`404`)
- Unhandled server errors (`500`)

## CORS

Allowed origins configured in app:

- `http://localhost:3000`
- `http://localhost:5173`
