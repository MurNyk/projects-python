import sqlite3
from datetime import datetime

def create_database():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            article TEXT  -- Добавляем столбец для артикула
        )
    ''')
    connection.commit()
    connection.close()

def create_order_table():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            company_name TEXT,
            delivery_address TEXT NOT NULL,
            expected_date TEXT NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            status TEXT DEFAULT 'в обработке',
            delivered_date TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')
    connection.commit()
    connection.close()

def create_client_product_table():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS client_product_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            product_price REAL NOT NULL,
            shopping_price REAL NOT NULL,
            total_price REAL NOT NULL  -- Добавляем колонку для итоговой суммы
        )
    ''')
    connection.commit()
    connection.close()

def get_db_connection():
    """Создает и возвращает подключение к базе данных."""
    connection = sqlite3.connect("products.db")
    return connection

def create_business_trip_table():
    """Создает таблицу для командировок, если она не существует."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS business_trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            destination TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            trip_purpose TEXT NOT NULL,  -- Добавляем поле для цели поездки
            status TEXT DEFAULT 'Отправлен'
        )
    ''')
    connection.commit()
    connection.close()

# Функция для создания таблицы raw_materials
def create_raw_materials_table():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Создание таблицы, если её не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS raw_materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_name TEXT NOT NULL,    -- Название сырья
            article TEXT NOT NULL,          -- Артикул
            quantity INTEGER NOT NULL,      -- Количество поступившего сырья
            output_quantity REAL,           -- Масса выходного продукта
            supplier TEXT NOT NULL,         -- Поставщик
            delivery_date TEXT NOT NULL,    -- Дата поставки
            brigade TEXT NOT NULL,          -- Бригада
            start_date TEXT NOT NULL,       -- Дата начала выполнения
            final_product TEXT NOT NULL,    -- Что должно получиться в итоге
            processing_coefficient REAL NOT NULL,  -- Коэффициент переработки
            status TEXT NOT NULL            -- Статус
        )
    ''')
    
    connection.commit()
    connection.close()
#--------------------------------------------------------------------------------------------------------------#
def create_repair_table():
    """Создает таблицу для заявок на ремонт, если она не существует, с колонкой status."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS repairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repair_type TEXT NOT NULL,          -- Тип ремонта (автомобиль, инструмент, станок)
            item_name TEXT NOT NULL,            -- Модель автомобиля/инструмент/станок
            issue_description TEXT NOT NULL,    -- Описание поломки
            replacement_option TEXT,            -- Возможная замена
            repair_duration TEXT,               -- Срок ремонта
            created_at TEXT NOT NULL,           -- Дата создания заявки
            status TEXT DEFAULT 'не выполнено'  -- Статус заявки
        )
    ''')
    connection.commit()
    connection.close()

#--------------------------------------------------------------------------------------------------------------#

def add_business_trip(employee_name: str, destination: str, start_date: str, end_date: str, trip_purpose: str, status: str):
    """Добавляет новую командировку в базу данных."""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
        INSERT INTO business_trips (employee_name, destination, start_date, end_date, trip_purpose, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (employee_name, destination, start_date, end_date, trip_purpose, status))  # Добавляем цель поездки и статус

    connection.commit()
    connection.close()

def get_all_business_trips():
    """Получает все командировки из базы данных."""
    connection = get_db_connection()  # Подключаемся к базе данных
    cursor = connection.cursor()  # Создаем курсор для выполнения SQL-запросов
    cursor.execute("SELECT * FROM business_trips")  # Выбираем все записи из таблицы командировок
    business_trips = cursor.fetchall()  # Извлекаем все записи
    connection.close()  # Закрываем соединение с базой данных
    return business_trips  # Возвращаем список командировок


def update_business_trip_status(trip_id: int, new_status: str):
    """Обновляет статус командировки в базе данных."""
    connection = get_db_connection()
    cursor = connection.cursor()

    # Проверяем, существует ли колонка 'status'
    cursor.execute("PRAGMA table_info(business_trips)")
    columns = cursor.fetchall()

    # Если колонки 'status' нет, то добавляем её
    if not any(column[1] == 'status' for column in columns):
        cursor.execute('''
            ALTER TABLE business_trips ADD COLUMN status TEXT
        ''')

    # Обновляем статус командировки
    cursor.execute('''
        UPDATE business_trips SET status = ? WHERE id = ?
    ''', (new_status, trip_id))

    connection.commit()
    connection.close()


def add_client_product_data(client_name: str, product_name: str, quantity: int, product_price: float, shopping_price: float):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO client_product_data (client_name, product_name, quantity, product_price, shopping_price)
        VALUES (?, ?, ?, ?, ?)
    ''', (client_name, product_name, quantity, product_price, shopping_price))
    connection.commit()
    connection.close()


def get_client_product_data_from_orders():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT o.client_name, p.name, o.quantity
        FROM orders o
        JOIN products p ON o.product_id = p.id
    ''')
    data = cursor.fetchall()
    connection.close()
    return data

def add_product_to_db(name: str, quantity: int):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO products (name, quantity) VALUES (?, ?)", (name, quantity))
    connection.commit()
    connection.close()

def save_order_to_db(client_name: str, company_name: str, delivery_address: str, expected_date: str, product_id: int, quantity: int, product_price: float, shopping_price: float):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    # Сохранение данных в таблицу orders
    cursor.execute('''
        INSERT INTO orders (client_name, company_name, delivery_address, expected_date, product_id, quantity)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (client_name, company_name, delivery_address, expected_date, product_id, quantity))
    
    # Получаем имя продукта по его id
    cursor.execute("SELECT name FROM products WHERE id = ?", (product_id,))
    product_name = cursor.fetchone()[0]
    
    # Рассчитываем итоговую сумму
    total_price = (product_price * quantity) + shopping_price

    # Сохранение данных в таблицу client_product_data
    cursor.execute('''
        INSERT INTO client_product_data (client_name, product_name, quantity, product_price, shopping_price, total_price)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (client_name, product_name, quantity, product_price, shopping_price, total_price))

    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, quantity, article FROM products")  # Добавляем поле 'article'
    products = cursor.fetchall()  # Получение всех записей
    connection.close()
    return products

def get_all_client_product_data():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT client_name, product_name, quantity, product_price, shopping_price, total_price 
        FROM client_product_data
    ''')
    data = cursor.fetchall()
    connection.close()
    return data


def delete_product_from_db(product_id: int):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    connection.commit()
    connection.close()

def update_product_quantity(product_id: int, quantity: int):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?", (quantity, product_id))
    connection.commit()
    connection.close()

def get_product_quantity(product_id: int) -> int:
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
    quantity = cursor.fetchone()
    connection.close()
    return quantity[0] if quantity else 0

def get_all_orders():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT o.id, o.client_name, o.company_name, o.delivery_address, o.expected_date, p.name, o.quantity, o.status, o.delivered_date
        FROM orders o
        JOIN products p ON o.product_id = p.id
    ''')
    orders = cursor.fetchall()  # Получение всех записей
    connection.close()
    return orders


def update_order_status(order_id: int, new_status: str):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    
    # Устанавливаем дату доставки только при изменении статуса на "доставлен"
    delivered_date = datetime.now().strftime('%Y-%m-%d') if new_status == 'доставлен' else None

    cursor.execute("UPDATE orders SET status = ?, delivered_date = ? WHERE id = ?", (new_status, delivered_date, order_id))
    connection.commit()
    connection.close()


def get_delivered_orders():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT o.id, o.client_name, o.company_name, o.delivery_address, o.expected_date, p.name, o.quantity, o.delivered_date
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.status = 'доставлен'
    ''')
    delivered_orders = cursor.fetchall()  # Получение всех доставленных грузов
    connection.close()
    return delivered_orders

def get_delivered_product_statistics():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT p.name, SUM(o.quantity), COUNT(o.id)
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.status = 'доставлен'
        GROUP BY p.name
    ''')
    statistics = cursor.fetchall()  # Получение всех записей
    connection.close()
    return statistics

def search_orders_by_client_name(client_name: str):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT o.id, o.client_name, o.company_name, o.delivery_address, o.expected_date, p.name, o.quantity, o.status
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.client_name LIKE ?
    ''', (f'%{client_name}%',))
    orders = cursor.fetchall()
    connection.close()
    return orders

def get_business_trip_by_id(trip_id: int):
    """Получает командировку по ID."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM business_trips WHERE id = ?
    ''', (trip_id,))
    trip = cursor.fetchone()
    connection.close()
    return trip


#------------------------------------------------------#
def get_all_repair_requests():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM repairs')
    repair_requests = cursor.fetchall()
    connection.close()
    print("Заявки на ремонт:", repair_requests)  # Проверка данных
    return repair_requests

def reset_repair_table_id():
    """Сбрасывает автоинкремент ID в таблице repairs после удаления всех записей."""
    connection = get_db_connection()
    cursor = connection.cursor()
    # Сброс автоинкремента ID в таблице repairs
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='repairs'")
    connection.commit()
    connection.close()
    print("Автоинкремент для repairs сброшен.")

