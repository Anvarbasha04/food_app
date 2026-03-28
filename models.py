from database import get_db

def init_db():
    db = get_db()
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS cart(
        id INTEGER PRIMARY KEY,
        username TEXT,
        product_id INTEGER,
        name TEXT,
        price INTEGER
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY,
        username TEXT,
        total INTEGER
    )""")

    db.commit()
    db.close()