from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import hashlib

from database import get_db
from models import init_db

app = FastAPI()
init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---------------- PRODUCTS ----------------
foods = [
    {"id":1,"name":"Burger","price":120,"img":"burger.jpg"},
    {"id":2,"name":"Pizza","price":250,"img":"pizza.jpg"},
    {"id":3,"name":"Chicken","price":180,"img":"chicken.jpg"},
    {"id":4,"name":"Coke","price":60,"img":"coke.jpg"},
]

# ---------------- HELPERS ----------------
def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

# ---------------- HOME ----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return RedirectResponse("/login")

# ---------------- REGISTER ----------------
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    db = get_db()
    db.execute("INSERT INTO users VALUES (NULL, ?, ?)",
               (username, hash_pw(password)))
    db.commit()
    db.close()
    return RedirectResponse("/login", status_code=303)

# ---------------- LOGIN ----------------
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username=? AND password=?",
                      (username, hash_pw(password))).fetchone()
    db.close()

    if user:
        response = RedirectResponse("/dashboard", status_code=303)
        response.set_cookie("user", username)
        return response

    return templates.TemplateResponse("login.html",
        {"request": request, "error": "Invalid login"})

# ---------------- DASHBOARD ----------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, search: str = ""):
    filtered = [f for f in foods if search.lower() in f["name"].lower()]

    user = request.cookies.get("user")

    db = get_db()
    cart_count = db.execute("SELECT COUNT(*) FROM cart WHERE username=?",
                            (user,)).fetchone()[0]
    db.close()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "foods": filtered,
        "cart_count": cart_count
    })

# ---------------- ADD TO CART ----------------
@app.get("/add/{id}")
def add_cart(request: Request, id: int):
    user = request.cookies.get("user")

    for f in foods:
        if f["id"] == id:
            db = get_db()
            db.execute("INSERT INTO cart VALUES (NULL, ?, ?, ?, ?)",
                       (user, id, f["name"], f["price"]))
            db.commit()
            db.close()

    return RedirectResponse("/dashboard", status_code=303)

# ---------------- CART ----------------
@app.get("/cart", response_class=HTMLResponse)
def cart_page(request: Request):
    user = request.cookies.get("user")

    db = get_db()
    items = db.execute("SELECT * FROM cart WHERE username=?", (user,)).fetchall()
    total = sum(i["price"] for i in items)
    db.close()

    return templates.TemplateResponse("cart.html", {
        "request": request,
        "items": items,
        "total": total
    })

# ---------------- PAYMENT ----------------
@app.get("/pay")
def pay(request: Request):
    user = request.cookies.get("user")

    db = get_db()
    items = db.execute("SELECT * FROM cart WHERE username=?", (user,)).fetchall()
    total = sum(i["price"] for i in items)

    db.execute("INSERT INTO orders VALUES (NULL, ?, ?)", (user, total))
    db.execute("DELETE FROM cart WHERE username=?", (user,))
    db.commit()
    db.close()

    return RedirectResponse("/orders", status_code=303)

# ---------------- ORDERS ----------------
@app.get("/orders", response_class=HTMLResponse)
def orders(request: Request):
    user = request.cookies.get("user")

    db = get_db()
    orders = db.execute("SELECT * FROM orders WHERE username=?", (user,)).fetchall()
    db.close()

    return templates.TemplateResponse("orders.html", {
        "request": request,
        "orders": orders
    })