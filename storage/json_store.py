import json
import logging
from pathlib import Path


class JsonStore:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def _read(self):
        try:
            raw = self.path.read_text(encoding="utf-8").strip()
            if not raw:
                return []
            return json.loads(raw)
        except (json.JSONDecodeError, OSError) as exc:
            logging.error("Failed to read JSON store: %s", exc)
            return []

    def _write(self, tasks):
        self.path.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

    def replace_all(self, tasks):
        self._write(tasks)

    def list_tasks(self):
        return self._read()

    def get_task(self, task_id: int):
        for task in self._read():
            if task.get("id") == task_id:
                return task
        return None
