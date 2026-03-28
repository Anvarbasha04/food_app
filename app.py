from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import sqlite3

app = FastAPI()

# Static files (CSS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("shop.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- INIT DB ----------------
def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT,
        price INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- SAMPLE FOOD ----------------
food_items = [
    {"name": "Burger", "price": 120, "image": "/static/burger.jpg"},
    {"name": "Pizza", "price": 250, "image": "/static/pizza.jpg"},
    {"name": "Fried Chicken", "price": 180, "image": "/static/chicken.jpg"},
    {"name": "Fries", "price": 90, "image": "/static/fries.jpg"},
]

# ---------------- ROUTES ----------------

# HOME PAGE
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# REGISTER
@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    conn = get_db()
    conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return RedirectResponse("/", status_code=303)


# LOGIN
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()
    conn.close()

    if user:
        return RedirectResponse("/dashboard", status_code=303)
    return {"error": "Invalid credentials"}


# DASHBOARD (FOOD LIST)
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "foods": food_items
    })


# ADD TO CART
@app.get("/add-to-cart/{item}/{price}")
def add_to_cart(item: str, price: int):
    conn = get_db()
    conn.execute("INSERT INTO cart (item, price) VALUES (?, ?)", (item, price))
    conn.commit()
    conn.close()
    return RedirectResponse("/cart", status_code=303)


# VIEW CART
@app.get("/cart", response_class=HTMLResponse)
def view_cart(request: Request):
    conn = get_db()
    items = conn.execute("SELECT * FROM cart").fetchall()
    conn.close()

    total = sum([i["price"] for i in items])

    return templates.TemplateResponse("cart.html", {
        "request": request,
        "items": items,
        "total": total
    })


# PAYMENT PAGE
@app.get("/payment", response_class=HTMLResponse)
def payment(request: Request):
    return templates.TemplateResponse("payment.html", {"request": request})


# CLEAR CART (AFTER PAYMENT)
@app.get("/success")
def success():
    conn = get_db()
    conn.execute("DELETE FROM cart")
    conn.commit()
    conn.close()
    return {"message": "Order placed successfully 🎉"}