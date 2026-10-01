import re

from flask import Flask, flash, redirect, render_template, request, session, url_for
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
        if "utoronto" in form.email.data.lower():
            return redirect(url_for("chat"))
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


@app.route("/chat", methods=["GET", "POST"])
def chat():
    email = session.get("email", "")
    if "utoronto" not in email.lower():
        if request.method == "POST":
            return {"reply": "Please submit a valid UofT email first."}, 401
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template(
            "chat.html", name=session.get("name"), email=email
        )

    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "")
    if not isinstance(message, str) or not message.strip():
        return {"reply": "Please enter a message."}, 400

    message = message.strip()
    name_match = re.fullmatch(
        r"my name is\s+(.+?)[.!?]*", message, flags=re.IGNORECASE
    )
    if name_match:
        remembered_name = name_match.group(1).strip()
        if len(remembered_name) > 60:
            return {"reply": "That name is too long for me to remember."}, 400
        session["chat_name"] = remembered_name
        reply = f"Nice to meet you, {remembered_name}!"
    elif "what is my name" in message.lower():
        remembered_name = session.get("chat_name")
        if remembered_name:
            reply = f"Your name is {remembered_name}."
        else:
            reply = "I don't know your name yet."
    elif "hello" in message.lower():
        reply = "Hello!"
    else:
        reply = "I don't understand."

    return {"reply": reply}


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
