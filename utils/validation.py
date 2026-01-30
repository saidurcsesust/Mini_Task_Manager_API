from datetime import datetime


ALLOWED_STATUSES = {"todo", "in_progress", "done"}


def validate_status(status):
    return status in ALLOWED_STATUSES


def parse_due_date(value):
    if value is None or value == "":
        return None
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None
    return parsed
