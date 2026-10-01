from datetime import datetime, timezone

from flask import Flask, flash, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string"
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = EmailField(
        "What is your UofT Email address?", validators=[DataRequired(), Email()]
    )
    submit = SubmitField("Submit")

    def validate_email(self, field):
        if "utoronto" not in field.data.lower():
            raise ValidationError("Please enter a UofT email address.")


def current_utc_time():
    """Return the naive UTC datetime expected by Flask-Moment."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name!")
        session["name"] = form.name.data
        session["email"] = form.email.data
        return redirect(url_for("index"))

    return render_template(
        "index.html",
        form=form,
        name=session.get("name"),
        email=session.get("email"),
        current_time=current_utc_time(),
    )


@app.route("/user/<name>")
def user(name):
    return render_template(
        "user.html", name=name, current_time=current_utc_time()
    )
