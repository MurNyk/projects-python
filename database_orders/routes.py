from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from database import get_all_repair_requests, get_business_trip_by_id, add_business_trip, create_business_trip_table,add_product_to_db, get_all_products, delete_product_from_db, reset_repair_table_id, save_order_to_db, get_all_orders, search_orders_by_client_name, get_all_client_product_data, get_all_business_trips, update_business_trip_status #Hпортируйте нужные функции
from datetime import datetime
from database import get_db_connection, create_raw_materials_table, update_product_quantity, update_order_status, get_delivered_orders, get_delivered_product_statistics
from pdf_generator import generate_contract_pdf # Импортируем функцию для генерации PDF
from pdf_generator_coman import generate_business_trip_pdf
from pdf_generator_proizvod import generate_processing_pdf
import os
import sqlite3

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def read_index(request: Request, client_name: str = ""):
    if client_name:
        orders = search_orders_by_client_name(client_name)
    else:
        orders = get_all_orders()
    # Форматирование дат
    for i in range(len(orders)):
        expected_date = datetime.strptime(orders[i][4], '%Y-%m-%d')
        orders[i] = list(orders[i])
        orders[i][4] = expected_date.strftime('%d.%m.%Y')
    # Получаем данные из client_product_data
    client_product_data = get_all_client_product_data()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "orders": orders,
        "client_name": client_name,
        "client_product_data": client_product_data # Передаем данные из client_product_data
    })


@router.get("/current_time", response_class=JSONResponse)
async def get_current_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"current_time": current_time}

@router.get("/products", response_class=HTMLResponse)
async def read_products(request: Request):
    products = get_all_products() # Получаем все товары из базы данных
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@router.get("/manage_products", response_class=HTMLResponse)
async def manage_products(request: Request):
    products = get_all_products() # Получаем все товары из базы данных
    return templates.TemplateResponse("manage_products.html", {"request": request, "products": products})

@router.post("/add_product")
async def add_product(
    name: str = Form(...),
    quantity: int = Form(...),
    article: str = Form(None) # Артикул не является обязательным полем
):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO products (name, quantity, article) VALUES (?, ?, ?)", (name, quantity, article))
    connection.commit()
    connection.close()
    return RedirectResponse(url="/products", status_code=303)

@router.post("/delete_product/{product_id}")
async def delete_product(product_id: int):
    delete_product_from_db(product_id)
    return RedirectResponse(url="/products", status_code=303) # Перенаправление на страницу товаров после удаления

@router.post("/place_order")
async def place_order(
    client_name: str = Form(...),
    company_name: str = Form(...),
    delivery_address: str = Form(...),
    expected_date: str = Form(...),
    product_id: int = Form(...),
    quantity: int = Form(...),
    product_price: float = Form(...), # Добавляем цену за продукт
shopping_price: float = Form (...) # Добавляем цену за отправку
):
    save_order_to_db(client_name, company_name, delivery_address, expected_date, product_id, quantity, product_price,shopping_price) # сохраняем заказ
    update_product_quantity(product_id, quantity) # Уменьшаем количество товара в таблице продуктов
    return RedirectResponse(url="/manage_products", status_code=303) # Перенаправление на страницу управления товарами

@router.post("/update_order_status/{order_id}")
async def update_order_status_route(order_id: int, status: str = Form(...)):
    update_order_status(order_id, status) # обновляем статус заказа в базе данных
    return RedirectResponse(url="/", status_code=303) # Перенаправление на главную страницу

@router.get("/statistics", response_class=HTMLResponse)
async def statistics(request: Request):
    delivered_orders = get_delivered_orders() # Получаем только доставленные грузы
    product_statistics = get_delivered_product_statistics() # Получаем статистику по доставленным товарам
    return templates.TemplateResponse("statistics.html", {
        "request": request,
        "delivered_orders": delivered_orders,
        "product_statistics": product_statistics
    })

@router.get("/generate_contract/{client_name}/{product_name}/{quantity}/{product_price}/{total_price}")
async def generate_contract(client_name: str, product_name: str, quantity: int, product_price: float, total_price: float):
    # Генерация PDF-документа и получение пути к файлу
    file_path = generate_contract_pdf(client_name, product_name, quantity, product_price, total_price)

    # Проверка существования файла перед отправкой
    if not file_path or not isinstance(file_path, str) or not os.path.exists(file_path):
        return {"error": "Файл не найден или не был сгенерирован."}

    # Возвращаем PDF-файл пользователю
    response = FileResponse(path=file_path, filename=os.path.basename(file_path), media_type='application/pdf')
    
    # Удаляем файл после отправки (опционально)
    # os.remove(file_path)
    return response

# Маршрут для страницы "Командировка"
@router.get("/business_trip", response_class=HTMLResponse)
async def business_trip_page(request: Request):
    business_trips = get_all_business_trips()
    return templates.TemplateResponse("business_trip.html", {
        "request": request,
        "business_trips": business_trips
    })

@router.post("/finish_business_trip/{trip_id}")
async def finish_business_trip(trip_id: int):
    update_business_trip_status(trip_id, "закончил работу")
    return RedirectResponse(url="/business_trip", status_code=303)

@router.post("/submit_business_trip")
async def submit_business_trip(
    employee_name: str = Form(...),
    destination: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    trip_purpose: str = Form(...),
    status: str = Form(...)
):
    create_business_trip_table()
    add_business_trip(employee_name, destination, start_date, end_date, trip_purpose, status)
    return RedirectResponse(url="/business_trip", status_code=303)

# Маршрут для генерации PDF для командировки
@router.get("/generate_trip_pdf/{trip_id}")
async def generate_trip_pdf(trip_id: int):
    # Получаем данные командировки по ID
    trip = get_business_trip_by_id(trip_id)
    if not trip:
        return {"error": "Командировка не найдена"}
    # Генерируем PDF
    pdf_file_path = generate_business_trip_pdf(trip)
    # Возвращаем PDF файл пользователю
    return FileResponse(pdf_file_path, media_type="application/pdf", filename=f"business_trip_{trip_id}.pdf")


@router.get("/edit_product_quantity/{product_id}", response_class=HTMLResponse)

async def edit_product_quantity(request: Request, product_id: int):
    # Получаем данные о товаре по его ID
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, quantity FROM products WHERE id=?", (product_id,))
    product = cursor.fetchone()
    connection.close()
    if not product:
        return HTMLResponse("Товар не найден", status_code=404)
    return templates.TemplateResponse("edit_quantity.html", {
        "request": request,
        "product": product
    })

@router.post("/update_product_quantity/{product_id}")

async def update_product_quantity_route(product_id: int, quantity: int = Form(...)):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (quantity, product_id))
    connection.commit()
    connection.close()
    return RedirectResponse(url="/products", status_code=303)

# Маршрут для отображения страницы "Производство"
@router.get("/production", response_class=HTMLResponse)

async def production_page(request: Request):
    connection = get_db_connection()
    cursor = connection.cursor()
    # Получаем все записи из таблицы raw_materials, включая массу выходного продукта
    cursor.execute('SELECT * FROM raw_materials')
    raw_materials = cursor.fetchall()

    connection.close()

    # Передаем данные в шаблон для отображения
    return templates.TemplateResponse("production.html", {
        "request": request,
        "raw_materials": raw_materials
    })


# Маршрут для обработки формы поставки сырья
@router.post("/submit_raw_material")

async def submit_raw_material(
    material_name: str = Form(...),
    article: str = Form(...),
    quantity: int = Form(...),
    output_quantity: float = Form(...), # Новое поле
    supplier: str = Form(...),
    delivery_date: str = Form(...),
    brigade: str = Form(...),
    start_date: str = Form(...),
    final_product: str = Form(...),
    processing_coefficient: float = Form(...),
    status: str = Form(...)
):
    # Сохранение данных в базу данных
    connection = get_db_connection()
    cursor = connection.cursor()
    # Вставляем данные в таблицу raw_materials, включая массу выходного продукта
    cursor.execute('''
    INSERT INTO raw_materials (
        material_name, article, quantity, output_quantity, supplier, delivery_date, brigade, start_date, final_product, processing_coffficient, status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (material_name, article, quantity, output_quantity, supplier, delivery_date, brigade, start_date, final_product, processing_coefficient, status))
    connection.commit()
    connection.close()
    # Перенаправляем обратно на страницу производства
    return RedirectResponse(url="/production", status_code=303)
# Маршрут для обновления статуса
@router.post("/update_status/{material_id}")

async def update_status(material_id: int, status: str = Form(...)):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE raw_materials
        SET status = ?
        WHERE id = ?
    ''', (status, material_id))
    connection.commit()
    connection.close()

    # Перенаправляем обратно на страницу производства
    return RedirectResponse(url="/production", status_code=303)

# Маршрут для генерации документа о переработке
@router.get("/generate_processing_document/{material_id}")

async def generate_processing_document(material_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    # Получаем данные о материале по его ID
    cursor.execute('SELECT * FROM raw_materials WHERE id = ?', (material_id,))

async def update_status(material_id: int, status: str = Form(...)):
    # обновляем статус по ID
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
    UPDATE raw_materials
    SET status = ?
    WHERE id = ?
    ''', (status, material_id))
    connection.commit()
    connection.close()
    # Перенаправляем обратно на страницу производства
    return RedirectResponse(url="/production", status_code=303)

# Маршрут для генерации документа о переработке
@router.get("/generate_processing_document/{material_id}")

async def generate_processing_document(material_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    # Получаем данные о материале по его ID
    cursor.execute('SELECT * FROM raw_materials WHERE id = ?', (material_id,))
    material = cursor.fetchone()
    if not material:
        return {"error": "Материал не найден"}
    # Генерация PDF-документа с информацией о материале
    pdf_file_path = generate_processing_pdf(material)
    # Проверяем, существует ли файл перед отправкой
    if not os.path.exists(pdf_file_path):
        return {"error": "Не удалось создать документ"}
    # Отправляем PDF-файл пользователю
    return FileResponse(pdf_file_path, filename=os.path.basename(pdf_file_path), media_type='application/pdf')
@router.get("/repair", response_class=HTMLResponse)
async def repair_page(request: Request):
    repair_requests = get_all_repair_requests()
    return templates.TemplateResponse("repair.html", {"request": request, "repair_requests": repair_requests})


@router.post("/submit_repair_request")
async def submit_repair_request(
    repair_type: str = Form(...),
    vehicle_model: str = Form(None),
    vehicle_issue: str = Form(None),
    vehicle_replacement: str = Form(None),
    vehicle_repair_duration: str = Form(None),
    tool_type: str = Form(None),
    tool_issue: str = Form(None),
    tool_replacement: str = Form(None),
    tool_repair_duration: str = Form(None),
    machine_model: str = Form(None),
    machine_issue: str = Form(None),
    machine_replacement: str = Form(None),
    machine_repair_duration: str = Form(None)
):
    # Проверка на тип ремонта и выбор значений
    if repair_type == "vehicle":
        item_name = vehicle_model
        issue_description = vehicle_issue
        replacement_option = vehicle_replacement
        repair_duration = vehicle_repair_duration
    elif repair_type == "tools":
        item_name = tool_type
        issue_description = tool_issue
        replacement_option = tool_replacement
        repair_duration = tool_repair_duration
    elif repair_type == "machines":
        item_name = machine_model
        issue_description = machine_issue
        replacement_option = machine_replacement
        repair_duration = machine_repair_duration
    else:
        return {"error": "Неверный тип ремонта"}

    # Сохраняем данные в таблицу repairs
    try:
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO repairs (repair_type, item_name, issue_description, replacement_option, repair_duration, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (repair_type, item_name, issue_description, replacement_option, repair_duration, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            connection.commit()
            print(f"Заявка на ремонт {item_name} успешно сохранена.")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении заявки на ремонт: {e}")

    return RedirectResponse(url="/repair", status_code=303)

@router.post("/delete_repair/{repair_id}")
async def delete_repair_request(repair_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM repairs WHERE id = ?", (repair_id,))
    connection.commit()
    connection.close()
    return RedirectResponse(url="/repair", status_code=303)

@router.post("/clear_repair_requests")
async def clear_repair_requests():
    connection = get_db_connection()
    cursor = connection.cursor()
    # Удаление всех записей из таблицы repairs
    cursor.execute("DELETE FROM repairs")
    connection.commit()
    connection.close()
    
    # Сброс автоинкремента ID
    reset_repair_table_id()
    
    return RedirectResponse(url="/repair", status_code=303)

@router.post("/complete_repair/{repair_id}")
async def complete_repair(repair_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE repairs SET status = 'выполнено' WHERE id = ?", (repair_id,))
    connection.commit()
    connection.close()
    return RedirectResponse(url="/repair", status_code=303)

