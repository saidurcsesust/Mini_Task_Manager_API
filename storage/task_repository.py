import logging
from datetime import datetime, date

from sqlalchemy import or_, select

from storage.db import Task


class TaskRepository:
    def __init__(self, session_factory, json_store):
        self.session_factory = session_factory
        self.json_store = json_store
        self.logger = logging.getLogger(__name__)

    def _task_to_dict(self, task: Task):
        if isinstance(task.created_at, datetime):
            created_at = task.created_at.strftime("%d-%m-%Y")
        else:
            created_at = task.created_at
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "created_at": created_at,
            "due_date": task.due_date.isoformat() if isinstance(task.due_date, date) else task.due_date,
        }

    def create(self, title, description, due_date):
        with self.session_factory() as session:
            task = Task(title=title, description=description, status="todo", due_date=due_date)
            session.add(task)
            session.commit()
            session.refresh(task)
            result = self._task_to_dict(task)
        self._sync_json()
        self.logger.info("Repo created task %s", result["id"])
        return result

    def list(self, status=None, q=None, sort="created_at"):
        with self.session_factory() as session:
            stmt = select(Task)
            if status:
                stmt = stmt.where(Task.status == status)
            if q:
                pattern = f"%{q}%"
                stmt = stmt.where(or_(Task.title.ilike(pattern), Task.description.ilike(pattern)))
            if sort == "due_date":
                stmt = stmt.order_by(Task.due_date.is_(None), Task.due_date.asc(), Task.created_at.desc())
            elif sort == "id":
                stmt = stmt.order_by(Task.id.asc())
            else:
                stmt = stmt.order_by(Task.created_at.desc())
            tasks = session.execute(stmt).scalars().all()
        return [self._task_to_dict(task) for task in tasks]

    def get(self, task_id: int):
        with self.session_factory() as session:
            task = session.get(Task, task_id)
            return self._task_to_dict(task) if task else None

    def update(self, task_id: int, updates: dict):
        with self.session_factory() as session:
            task = session.get(Task, task_id)
            if not task:
                return None
            for key, value in updates.items():
                setattr(task, key, value)
            session.commit()
            session.refresh(task)
            result = self._task_to_dict(task)
        self._sync_json()
        self.logger.info("Repo updated task %s", task_id)
        return result

    def delete(self, task_id: int) -> bool:
        with self.session_factory() as session:
            task = session.get(Task, task_id)
            if not task:
                return False
            session.delete(task)
            session.commit()
        self._sync_json()
        self.logger.info("Repo deleted task %s", task_id)
        return True

    def _sync_json(self):
        tasks = self.list()
        self.json_store.replace_all(tasks)
        self.logger.info("Synced JSON store count=%s", len(tasks))
