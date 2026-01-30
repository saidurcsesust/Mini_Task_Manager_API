import logging

from flask import Flask, jsonify, request

from routes.api import api_bp
from routes.web import web_bp
from storage.db import init_db, init_engine, make_session_factory
from storage.json_store import JsonStore
from storage.task_repository import TaskRepository


def create_app():
    app = Flask(__name__)

    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")

    engine = init_engine()
    init_db(engine)
    session_factory = make_session_factory(engine)
    json_store = JsonStore("data/tasks.json")
    app.config["repo"] = TaskRepository(session_factory, json_store)

    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)

    @app.errorhandler(404)
    def handle_not_found(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Not found"}), 404
        return error

    @app.errorhandler(500)
    def handle_server_error(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Server error"}), 500
        return error

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
