# Mini Task Manager API

## Local setup (SQLite via SQLAlchemy)

1) Install dependencies:
```
pip install -r requirements.txt
```

2) Optional: set a custom DB path (defaults to `data/tasks.db`):
```
export DATABASE_URL=sqlite:///data/tasks.db
```

3) Run the app:
```
python app.py
```

## Seed dummy data

```
python scripts/seed_data.py
```

Add `--force` to seed even if tasks already exist.

## API quick check

Create:
```
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk","description":"2 liters","due_date":"2026-02-05"}'
```

List:
```
curl http://localhost:5000/api/tasks
```
