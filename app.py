from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Хранилище задач (в памяти)
tasks = []

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Получение списка задач
@app.route('/get-tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Добавление новой задачи
@app.route('/add-task', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Заголовок задачи обязателен'}), 400

    task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'completed': False
    }
    tasks.append(task)
    return jsonify(task=task), 201

# Обновление статуса задачи
@app.route('/update-task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = data.get('completed', task['completed'])
            return jsonify(task=task)
    return jsonify({'error': 'Задача не найдена'}), 404

# Удаление задачи
@app.route('/delete-task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)