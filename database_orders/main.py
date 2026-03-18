from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import create_database
from routes import router
from database import create_database,create_order_table, create_client_product_table,create_business_trip_table,create_raw_materials_table,create_repair_table

app = FastAPI()
templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="static"), name = "static")

app.include_router(router)
    

if __name__ == "__main__":
    import uvicorn
    create_database()
    create_order_table()
    create_client_product_table()
    create_business_trip_table()
    create_raw_materials_table()
    create_repair_table()
    uvicorn.run(app,host= "127.0.0.1",port = 8001)    