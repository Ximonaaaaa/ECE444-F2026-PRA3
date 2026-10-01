from flask import Flask, flash, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string"
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = EmailField(
        "What is your UofT Email address?", validators=[DataRequired(), Email()]
    )
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        old_email = session.get("email")
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name!")
        if old_email is not None and old_email != form.email.data:
            flash("Looks like you have changed your email!")
        session["name"] = form.name.data
        session["email"] = form.email.data
        return redirect(url_for("index"))

    email = session.get("email")
    return render_template(
        "index.html",
        form=form,
        name=session.get("name"),
        email=email,
        is_uoft_email=email is not None and "utoronto" in email.lower(),
    )


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name)
