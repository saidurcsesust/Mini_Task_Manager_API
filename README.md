# Mini Task Manager API

A small Flask app with a JSON/SQLite-backed task repository, REST API, and a live-updating web UI.

- API base: `http://127.0.0.1:5000/api`
- UI: `http://127.0.0.1:5000/tasks`

## Features

- Create, list, update, delete tasks
- Filter by status and search by text
- Sort by `created_at` or `due_date`
- Live-updating UI with status toggle (todo → in_progress → done)

## Requirements

- Python 3.9+
- pip

## Clone and setup

```bash
git clone https://github.com/saidurcsesust/Mini_Task_Manager_API.git
cd Mini_Task_Manager_API

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Environment

By default the app uses SQLite at `data/tasks.db`.

Optional custom DB path:

```bash
export DATABASE_URL=sqlite:///data/tasks.db
```

## Run the app

```bash
flask run
```

The server listens on `http://127.0.0.1:5000`.

## Seed dummy data

```bash
python scripts/seed_data.py
```

Add `--force` to overwrite existing data.

## API Reference

### Create a task

- Endpoint: `POST /api/tasks`
- Body:
  - `title` (string, required)
  - `description` (string, optional)
  - `status` (todo, in_progress, done)​
  - `due_date` (string, optional, format `YYYY-MM-DD`)

```bash
curl -i -X POST http://127.0.0.1:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy oil","description":"2 liters","due_date":"2026-02-05"}'
```

### Get all tasks

```bash
curl -i http://127.0.0.1:5000/api/tasks
```

### Get a task by id

```bash
curl -i http://127.0.0.1:5000/api/tasks/1
```

### Update a task

```bash
curl -i -X PUT http://127.0.0.1:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy oil","description":"2 liters","status":"in_progress","due_date":"2026-02-05"}'
```

### Delete a task

```bash
curl -i -X DELETE http://127.0.0.1:5000/api/tasks/1
```

### List tasks

- Endpoint: `GET /api/tasks`
- Query params:
  - `status` = `todo` | `in_progress` | `done`
  - `q` = search text (matches title or description)
  - `sort` = `created_at` | `due_date` | `id`

Filter + sort examples:

```bash
curl -i "http://127.0.0.1:5000/api/tasks?status=todo"

curl -i "http://127.0.0.1:5000/api/tasks?q=oil&sort=due_date"

curl -i "http://127.0.0.1:5000/api/tasks?sort=id"
```

### Get a single task

- Endpoint: `GET /api/tasks/<id>`

```bash
curl -i http://127.0.0.1:5000/api/tasks/1
```

### Update a task

- Endpoint: `PUT /api/tasks/<id>`
- Body fields (all optional):
  - `title`
  - `description`
  - `status` = `todo` | `in_progress` | `done`
  - `due_date` (format `YYYY-MM-DD` or `null`)

```bash
curl -i -X PUT http://127.0.0.1:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy oil","description":"2 liters","status":"in_progress","due_date":"2026-02-05"}'
```

Clear due date:

```bash
curl -i -X PUT http://127.0.0.1:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"due_date":null}'
```

### Delete a task

- Endpoint: `DELETE /api/tasks/<id>`

```bash
curl -i -X DELETE http://127.0.0.1:5000/api/tasks/1
```


### Toggle task status (todo → in_progress → done → todo)

- Endpoint: `POST /tasks/<id>/toggle`

```bash
curl -i -X POST http://127.0.0.1:5000/tasks/1/toggle
```

## Notes

- `created_at` is formatted as `dd-mm-yyyy` in API responses.
- `due_date` expects input in `YYYY-MM-DD` format.
