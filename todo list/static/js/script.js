document.addEventListener('DOMContentLoaded', function() {
    const taskInput = document.getElementById('taskInput');
    const addTaskButton = document.getElementById('addTaskButton');
    const taskList = document.getElementById('taskList');

    // Функция для загрузки задач с сервера
    function loadTasks() {
        fetch('/get-tasks')
            .then(response => response.json())
            .then(data => {
                taskList.innerHTML = "";
                data.forEach(task => { // Исправлено: убрали .tasks
                    addTaskToDOM(task);
                });
            });
    }

    // Добавление задачи в DOM
    function addTaskToDOM(task) {
        const li = document.createElement('li');
        li.className = 'task-item';
        li.dataset.id = task.id;
        if (task.completed) {
            li.classList.add('completed');
        }
        li.innerHTML = `
            <span>${task.title}</span>
            <button class="delete-button">Удалить</button>
        `;

        // Обработчик клика по задаче (отметить выполненной)
        li.addEventListener('click', function(e) {
            if (e.target.classList.contains('delete-button')) {
                // Удаление задачи
                deleteTask(task.id);
            } else {
                // Обновление статуса задачи
                toggleTaskCompletion(task.id, !task.completed); // Изменено на !task.completed
            }
        });
        taskList.appendChild(li);
    }

    // Добавление новой задачи
    addTaskButton.addEventListener('click', function() {
        const title = taskInput.value.trim();
        if (title) {
            fetch('/add-task', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title })
            })
            .then(response => response.json())
            .then(data => {
                addTaskToDOM(data.task);
                taskInput.value = "";
            });
        }
    });

    // Обновление статуса задачи
    function toggleTaskCompletion(taskId, completed) {
        fetch('/update-task/' + taskId, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ completed })
        })
        .then(response => response.json())
        .then(data => {
            const taskItem = document.querySelector(`li[data-id="${taskId}"]`); // Исправлено
            if (completed) {
                taskItem.classList.add('completed');
            } else {
                taskItem.classList.remove('completed');
            }
        });
    }

    // Удаление задачи
    function deleteTask(taskId) {
        fetch(`/delete-task/${taskId}`, { // Исправлено
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            const taskItem = document.querySelector(`li[data-id="${taskId}"]`); // Исправлено
            taskItem.remove();
        });
    }

    // Загрузка задач при загрузке страницы
    loadTasks();
});