from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Templates & Static
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Dummy user
USER = {"username": "admin", "password": "1234"}

# Food data
foods = [
    {"id": 1, "name": "Burger", "price": 120, "image": "/static/images/burger.jpg"},
    {"id": 2, "name": "Pizza", "price": 250, "image": "/static/images/pizza.jpg"},
    {"id": 3, "name": "Chicken", "price": 180, "image": "/static/images/chicken.jpg"},
]

cart = []

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == USER["username"] and password == USER["password"]:
        return RedirectResponse(url="/dashboard", status_code=303)
    return RedirectResponse(url="/", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "foods": foods,
        "cart": cart
    })

@app.get("/add_to_cart/{food_id}")
async def add_to_cart(food_id: int):
    for food in foods:
        if food["id"] == food_id:
            cart.append(food)
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/payment", response_class=HTMLResponse)
async def payment(request: Request):
    total = sum(item["price"] for item in cart)
    return templates.TemplateResponse("payment.html", {
        "request": request,
        "cart": cart,
        "total": total
    })