from flask import render_template, request, url_for, flash, redirect, Flask
from app import app, db
from models import Message
from async_tasks import save_message_async

@app.route("/")
def home():
    all_messages = Message.query.all()
    return render_template("index.html", messages=all_messages)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            title = data.get('title')
            content = data.get('content')
        else:
            title = request.form['title']
            content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            new_message = Message(title=title, content=content)
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('create.html')


@app.route("/create-async/", methods=["GET", "POST"])
def create_async():
    if request.method == "POST":
        if not request.is_json:
            return {"status": "error", "message": "Content-Type must be application/json"}, 400

        data = request.get_json(silent=True)
        if not data:
            return {"status": "error", "message": "Invalid JSON"}, 400

        title = data.get("title")
        content = data.get("content")
        if not title or not content:
            return {"status": "error", "message": "Missing fields"}, 400

        save_message_async.delay(title, content)
        return {"status": "ok", "message": "Task queued"}, 202

    return render_template("create_async.html")


@app.route('/loaderio-1cce1e84eaa35557ea6fe6171d28f44c.html')
def loaderio_verification():
    return "loaderio-1cce1e84eaa35557ea6fe6171d28f44c"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=8888)
