import logging

from flask import Blueprint, current_app, redirect, render_template, request, url_for

from utils.validation import validate_status


web_bp = Blueprint("web", __name__)
logger = logging.getLogger(__name__)


def _repo():
    return current_app.config["repo"]


@web_bp.route("/")
def home():
    return render_template("index.html")


@web_bp.route("/tasks", methods=["GET", "POST"])
def tasks_page():
    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        description = request.form.get("description") or None
        due_date = request.form.get("due_date") or None
        status = request.form.get("status") or "todo"
        if title:
            from utils.validation import parse_due_date

            parsed_due = parse_due_date(due_date)
            task = _repo().create(title, description, parsed_due)
            if status != "todo":
                _repo().update(task["id"], {"status": status})
            logger.info("Created task via UI %s", task["id"])
        return redirect(url_for("web.tasks_page"))

    status = request.args.get("status")
    if status and not validate_status(status):
        status = None
    from datetime import date

    tasks = _repo().list(status=status)
    logger.info("Rendered tasks page count=%s", len(tasks))
    return render_template(
        "tasks.html",
        tasks=tasks,
        status=status,
        today=date.today().isoformat(),
    )


@web_bp.route("/tasks/<int:task_id>/done", methods=["POST"])
def mark_done(task_id: int):
    _repo().update(task_id, {"status": "done"})
    logger.info("Marked task done via UI %s", task_id)
    return redirect(url_for("web.tasks_page"))
