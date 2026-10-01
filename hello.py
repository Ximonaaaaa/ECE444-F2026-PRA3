from datetime import datetime, timezone

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


def current_utc_time():
    """Return the naive UTC datetime expected by Flask-Moment."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


@app.route("/")
def index():
    return render_template(
        "index.html", name="Simona", current_time=current_utc_time()
    )


@app.route("/user/<name>")
def user(name):
    return render_template(
        "user.html", name=name, current_time=current_utc_time()
    )
