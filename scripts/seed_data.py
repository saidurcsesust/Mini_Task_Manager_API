import argparse
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app
from utils.validation import parse_due_date


def main():
    parser = argparse.ArgumentParser(description="Seed dummy tasks")
    parser.add_argument("--force", action="store_true", help="Seed even if tasks already exist")
    args = parser.parse_args()

    app = create_app()
    repo = app.config["repo"]

    existing = repo.list()
    if existing and not args.force:
        print(f"Seed skipped: {len(existing)} task(s) already exist. Use --force to add more.")
        return

    samples = [
        {
            "title": "Buy milk",
            "description": "2 liters",
            "due_date": "2026-02-05",
        },
        {
            "title": "Finish report",
            "description": "Draft v1 for Q1",
            "due_date": "2026-02-10",
        },
        {
            "title": "Gym session",
            "description": "Leg day workout",
            "due_date": None,
        },
        {
            "title": "Book dentist appointment",
            "description": "Call Dr. Lee",
            "due_date": "2026-02-15",
        },
    ]

    for task in samples:
        due_date = parse_due_date(task["due_date"])
        repo.create(task["title"], task["description"], due_date)

    print(f"Seeded {len(samples)} tasks.")


if __name__ == "__main__":
    main()
