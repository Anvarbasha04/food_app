from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import engine, SessionLocal
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

foods = [
    {"id": 1, "name": "Burger", "price": 120, "image": "/static/images/burger.jpg"},
    {"id": 2, "name": "Pizza", "price": 250, "image": "/static/images/pizza.jpg"},
]

# HOME
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# REGISTER
@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = models.User(username=username, password=password)
    db.add(user)
    db.commit()
    return RedirectResponse("/", status_code=303)

# LOGIN
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = db.query(models.User).filter_by(username=username, password=password).first()
    if user:
        return RedirectResponse("/dashboard", status_code=303)
    return RedirectResponse("/", status_code=303)

# DASHBOARD
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "foods": foods
    })

# ADD TO CART
@app.get("/add/{name}/{price}")
def add_cart(name: str, price: int):
    db = SessionLocal()
    item = models.Cart(food_name=name, price=price)
    db.add(item)
    db.commit()
    return RedirectResponse("/cart", status_code=303)

# CART
@app.get("/cart", response_class=HTMLResponse)
def cart(request: Request):
    db = SessionLocal()
    items = db.query(models.Cart).all()
    total = sum(item.price for item in items)
    return templates.TemplateResponse("cart.html", {
        "request": request,
        "cart": items,
        "total": total
    })

# PAYMENT
@app.get("/payment", response_class=HTMLResponse)
def payment(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})