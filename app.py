
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import uuid

app = Flask(__name__)

tasks = []

def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    filter_type = request.args.get("filter", "all")

    if request.method == "POST":
        task_text = request.form.get("task")
        if task_text:
            tasks.append({
                "id": str(uuid.uuid4()),
                "text": task_text,
                "done": False,
                "created_at": datetime.now().strftime("%d-%m-%Y %H:%M")
            })
        return redirect(url_for("index"))

    if filter_type == "completed":
        filtered_tasks = [t for t in tasks if t["done"]]
    elif filter_type == "pending":
        filtered_tasks = [t for t in tasks if not t["done"]]
    else:
        filtered_tasks = tasks

    return render_template("index.html", tasks=filtered_tasks, filter_type=filter_type)

@app.route("/toggle/<task_id>")
def toggle(task_id):
    task = get_task(task_id)
    if task:
        task["done"] = not task["done"]
    return redirect(url_for("index"))

@app.route("/delete/<task_id>")
def delete(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
