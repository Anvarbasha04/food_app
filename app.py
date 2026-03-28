from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

# Check folders exist (IMPORTANT)
if not os.path.exists("static"):
    os.mkdir("static")

if not os.path.exists("templates"):
    os.mkdir("templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

products = [
    {"id": 1, "name": "Burger", "price": 120, "image": "/static/burger.jpg"},
    {"id": 2, "name": "Pizza", "price": 250, "image": "/static/pizza.jpg"},
    {"id": 3, "name": "Pasta", "price": 180, "image": "/static/pasta.jpg"},
]

cart = []

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "products": products
    })

@app.get("/cart", response_class=HTMLResponse)
def view_cart(request: Request):
    total = sum(item["price"] for item in cart)
    return templates.TemplateResponse("cart.html", {
        "request": request,
        "cart": cart,
        "total": total
    })

@app.get("/add/{item_id}")
def add_to_cart(item_id: int):
    for p in products:
        if p["id"] == item_id:
            cart.append(p)
    return {"message": "Added"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)