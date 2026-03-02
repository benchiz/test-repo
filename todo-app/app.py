# app.py
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)


# Хранилище задач (в реальном проекте использовалась бы БД)
tasks = [
    {'id': 1, 'title': 'Изучить Flask', 'done': False, 'created': '2024-01-15'},
    {'id': 2, 'title': 'Создать Todo приложение', 'done': True, 'created': '2024-01-14'}
]


@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        new_id = max([task['id'] for task in tasks] + [0]) + 1
        tasks.append({
            'id': new_id,
            'title': title,
            'done': False,
            'created': datetime.now().strftime('%Y-%m-%d')
        })
    return redirect(url_for('index'))


@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = not task['done']
            break
    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)