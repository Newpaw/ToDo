from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)
    created_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(
        db.DateTime, nullable=True)


@app.route("/")
def index():
    incomplete = Todo.query.filter_by(completed=False)
    complete = Todo.query.filter_by(completed=True)
    # for test if exist some incomplete task
    exist = Todo.query.filter_by(completed=False).first()
    return render_template("index.html", incomplete=incomplete, complete=complete, exist=exist)


@app.route("/add", methods=["POST"])
def add():
    text = request.form["todoitem"]
    todo = Todo(text=text)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update", methods=["POST"])
def update():
    
    req_done = request.form.getlist("done")
    # req_update = request.form.getlist("update")
    # req_cancel = request.form.getlist("cancel")

    if req_done:
        todo = Todo.query.filter_by(id=int(req_done[0])).first()
        todo.completed = True
        todo.update_date = datetime.now()
        db.session.commit()

    # elif req_update:
    #     print(req_update)
    # else:
    #     print(req_cancel)

    
    return redirect(url_for("index"))
