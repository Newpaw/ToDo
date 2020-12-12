from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    completed = db.Column(db.Boolean)
    created_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)


@app.route("/")
def index():
    incomplete = Todo.query.filter_by(completed=False)
    complete = Todo.query.filter_by(completed=True)
    print(incomplete)
    return render_template("index.html", incomplete=incomplete, complete=complete)


@app.route("/add", methods=["POST"])
def add():
    text = request.form["todoitem"]
    todo = Todo(text=text, completed=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update", methods=["POST"])
def update():
    checkedlist = request.form.getlist("checked")
    # change the checked item in db to True
    for checked in checkedlist:
        todo = Todo.query.filter_by(id=int(checked)).first()
        todo.completed = True
        db.session.commit()
    return redirect(url_for("index"))
