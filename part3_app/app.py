import os

from flask import Flask

from .config import Config
from .models import db
from .resources import register_resource_routes


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True, template_folder="templates", static_folder="static")
    app.config.from_object(Config)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.database_uri(app.instance_path)

    db.init_app(app)
    app.jinja_env.globals["getattr"] = getattr
    register_resource_routes(app)

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)

