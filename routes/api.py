import logging

from flask import Blueprint, current_app, jsonify, request

from utils.validation import parse_due_date, validate_status


api_bp = Blueprint("api", __name__, url_prefix="/api")
logger = logging.getLogger(__name__)


def _repo():
    return current_app.config["repo"]


def _error(message, code):
    return jsonify({"error": message}), code


@api_bp.route("/tasks", methods=["POST"])
def create_task():
    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    if not title:
        return _error("Missing title", 400)
    description = payload.get("description")
    due_date_raw = payload.get("due_date")
    due_date = parse_due_date(due_date_raw) if due_date_raw is not None else None
    if due_date_raw is not None and due_date is None:
        return _error("Invalid due_date", 400)

    task = _repo().create(title, description, due_date)
    logger.info("Created task %s", task["id"])
    return jsonify(task), 201


@api_bp.route("/tasks", methods=["GET"])
def list_tasks():
    status = request.args.get("status")
    q = request.args.get("q")
    sort = request.args.get("sort", "created_at")

    if status and not validate_status(status):
        return _error("Invalid status", 400)
    if sort not in {"due_date", "created_at"}:
        sort = "created_at"

    tasks = _repo().list(status=status, q=q, sort=sort)
    logger.info("Listed tasks count=%s", len(tasks))
    return jsonify(tasks), 200


@api_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id: int):
    task = _repo().get(task_id)
    if not task:
        return _error("Task not found", 404)
    logger.info("Fetched task %s", task_id)
    return jsonify(task), 200


@api_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id: int):
    payload = request.get_json(silent=True) or {}
    updates = {}

    if "title" in payload:
        title = (payload.get("title") or "").strip()
        if not title:
            return _error("Missing title", 400)
        updates["title"] = title

    if "description" in payload:
        updates["description"] = payload.get("description")

    if "status" in payload:
        status = payload.get("status")
        if not validate_status(status):
            return _error("Invalid status", 400)
        updates["status"] = status

    if "due_date" in payload:
        due_date_raw = payload.get("due_date")
        due_date = parse_due_date(due_date_raw)
        if due_date_raw is not None and due_date is None:
            return _error("Invalid due_date", 400)
        updates["due_date"] = due_date

    task = _repo().update(task_id, updates)
    if not task:
        return _error("Task not found", 404)
    logger.info("Updated task %s", task_id)
    return jsonify(task), 200


@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    deleted = _repo().delete(task_id)
    if not deleted:
        return _error("Task not found", 404)
    logger.info("Deleted task %s", task_id)
    return jsonify({"deleted": True}), 200
