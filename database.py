import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


class Database:
    def __init__(self):
        self.path = Path(__file__).with_name("food_delivery.db")
        self.create_schema()
        self.seed()

    def connect(self):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def create_schema(self):
        with self.connect() as con:
            con.executescript(
                """
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE,
                    address TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS couriers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE,
                    transport TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Вільний'
                );

                CREATE TABLE IF NOT EXISTS menu_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL CHECK(price >= 0),
                    active INTEGER NOT NULL DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    courier_id INTEGER,
                    status TEXT NOT NULL DEFAULT 'Нове',
                    total REAL NOT NULL DEFAULT 0,
                    delivery_fee REAL NOT NULL DEFAULT 60,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(customer_id) REFERENCES customers(id),
                    FOREIGN KEY(courier_id) REFERENCES couriers(id)
                );

                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    menu_item_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL CHECK(quantity > 0),
                    price REAL NOT NULL CHECK(price >= 0),
                    FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE,
                    FOREIGN KEY(menu_item_id) REFERENCES menu_items(id)
                );
                """
            )

    def seed(self):
        with self.connect() as con:
            if con.execute("SELECT COUNT(*) FROM menu_items").fetchone()[0] == 0:
                con.executemany(
                    "INSERT INTO menu_items(name, category, price) VALUES(?,?,?)",
                    [
                        ("Маргарита", "Піца", 210),
                        ("Пепероні", "Піца", 260),
                        ("Чізбургер", "Бургери", 190),
                        ("Цезар з куркою", "Салати", 175),
                        ("Рамен з куркою", "Азійська кухня", 230),
                        ("Картопля фрі", "Закуски", 95),
                        ("Лимонад", "Напої", 75),
                        ("Тірамісу", "Десерти", 140),
                    ],
                )
            if con.execute("SELECT COUNT(*) FROM couriers").fetchone()[0] == 0:
                con.executemany(
                    "INSERT INTO couriers(name, phone, transport, status) VALUES(?,?,?,?)",
                    [
                        ("Андрій Коваленко", "+380501112233", "Авто", "Вільний"),
                        ("Максим Бондар", "+380671234567", "Велосипед", "На доставці"),
                        ("Олег Ткаченко", "+380931112244", "Скутер", "Вільний"),
                    ],
                )
            if con.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 0:
                con.executemany(
                    "INSERT INTO customers(name, phone, address) VALUES(?,?,?)",
                    [
                        ("Ірина Савчук", "+380991010101", "вул. Соборності, 42"),
                        ("Дмитро Мельник", "+380661212121", "вул. Європейська, 18"),
                        ("Марія Левченко", "+380731313131", "вул. Героїв АТО, 7"),
                    ],
                )
            if con.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0:
                customers = con.execute("SELECT id FROM customers ORDER BY id").fetchall()
                couriers = con.execute("SELECT id FROM couriers ORDER BY id").fetchall()
                items = con.execute("SELECT id, price FROM menu_items ORDER BY id").fetchall()
                samples = [
                    (customers[0][0], couriers[0][0], "Доставлено", 470, 60, datetime.now() - timedelta(hours=5)),
                    (customers[1][0], couriers[1][0], "В дорозі", 440, 60, datetime.now() - timedelta(hours=2)),
                    (customers[2][0], None, "Готується", 365, 60, datetime.now() - timedelta(minutes=45)),
                ]
                for index, row in enumerate(samples):
                    cur = con.execute(
                        "INSERT INTO orders(customer_id, courier_id, status, total, delivery_fee, created_at) VALUES(?,?,?,?,?,?)",
                        (row[0], row[1], row[2], row[3], row[4], row[5].strftime("%Y-%m-%d %H:%M:%S")),
                    )
                    con.execute(
                        "INSERT INTO order_items(order_id, menu_item_id, quantity, price) VALUES(?,?,?,?)",
                        (cur.lastrowid, items[index][0], 1, items[index][1]),
                    )

    def dashboard(self):
        with self.connect() as con:
            today = datetime.now().strftime("%Y-%m-%d")
            orders_today = con.execute("SELECT COUNT(*) FROM orders WHERE date(created_at)=?", (today,)).fetchone()[0]
            revenue = con.execute("SELECT COALESCE(SUM(total),0) FROM orders WHERE date(created_at)=? AND status!='Скасовано'", (today,)).fetchone()[0]
            active = con.execute("SELECT COUNT(*) FROM orders WHERE status IN ('Нове','Готується','В дорозі')").fetchone()[0]
            free_couriers = con.execute("SELECT COUNT(*) FROM couriers WHERE status='Вільний'").fetchone()[0]
            avg = con.execute("SELECT COALESCE(AVG(total),0) FROM orders WHERE status!='Скасовано'").fetchone()[0]
            return {
                "orders_today": orders_today,
                "revenue": revenue,
                "active": active,
                "free_couriers": free_couriers,
                "avg": avg,
            }

    def recent_orders(self, limit=8):
        with self.connect() as con:
            return con.execute(
                """
                SELECT o.id, c.name customer, o.status, o.total, o.created_at,
                       COALESCE(cr.name, 'Не призначено') courier
                FROM orders o
                JOIN customers c ON c.id=o.customer_id
                LEFT JOIN couriers cr ON cr.id=o.courier_id
                ORDER BY o.id DESC LIMIT ?
                """,
                (limit,),
            ).fetchall()

    def orders(self, search="", status="Усі"):
        with self.connect() as con:
            sql = """
                SELECT o.id, c.name customer, c.phone, c.address, o.status,
                       o.total, o.created_at, COALESCE(cr.name, 'Не призначено') courier
                FROM orders o
                JOIN customers c ON c.id=o.customer_id
                LEFT JOIN couriers cr ON cr.id=o.courier_id
                WHERE (c.name LIKE ? OR c.phone LIKE ? OR CAST(o.id AS TEXT) LIKE ?)
            """
            params = [f"%{search}%", f"%{search}%", f"%{search}%"]
            if status != "Усі":
                sql += " AND o.status=?"
                params.append(status)
            sql += " ORDER BY o.id DESC"
            return con.execute(sql, params).fetchall()

    def order_items(self, order_id):
        with self.connect() as con:
            return con.execute(
                """
                SELECT m.name, oi.quantity, oi.price, oi.quantity*oi.price subtotal
                FROM order_items oi
                JOIN menu_items m ON m.id=oi.menu_item_id
                WHERE oi.order_id=?
                """,
                (order_id,),
            ).fetchall()

    def menu(self, active_only=False):
        with self.connect() as con:
            sql = "SELECT * FROM menu_items"
            if active_only:
                sql += " WHERE active=1"
            sql += " ORDER BY category, name"
            return con.execute(sql).fetchall()

    def couriers(self):
        with self.connect() as con:
            return con.execute("SELECT * FROM couriers ORDER BY name").fetchall()

    def customers(self, search=""):
        with self.connect() as con:
            return con.execute(
                """
                SELECT c.id, c.name, c.phone, c.address,
                       COUNT(o.id) orders_count, COALESCE(SUM(o.total),0) spent
                FROM customers c
                LEFT JOIN orders o ON o.customer_id=c.id AND o.status!='Скасовано'
                WHERE c.name LIKE ? OR c.phone LIKE ?
                GROUP BY c.id
                ORDER BY c.id DESC
                """,
                (f"%{search}%", f"%{search}%"),
            ).fetchall()

    def find_or_create_customer(self, name, phone, address):
        with self.connect() as con:
            row = con.execute("SELECT id FROM customers WHERE phone=?", (phone,)).fetchone()
            if row:
                con.execute("UPDATE customers SET name=?, address=? WHERE id=?", (name, address, row[0]))
                return row[0]
            cur = con.execute("INSERT INTO customers(name, phone, address) VALUES(?,?,?)", (name, phone, address))
            return cur.lastrowid

    def create_order(self, customer_id, courier_id, cart, delivery_fee=60):
        subtotal = sum(item["price"] * item["quantity"] for item in cart)
        total = subtotal + delivery_fee
        with self.connect() as con:
            cur = con.execute(
                "INSERT INTO orders(customer_id, courier_id, status, total, delivery_fee, created_at) VALUES(?,?,?,?,?,?)",
                (customer_id, courier_id, "Нове", total, delivery_fee, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            )
            order_id = cur.lastrowid
            con.executemany(
                "INSERT INTO order_items(order_id, menu_item_id, quantity, price) VALUES(?,?,?,?)",
                [(order_id, item["id"], item["quantity"], item["price"]) for item in cart],
            )
            if courier_id:
                con.execute("UPDATE couriers SET status='На доставці' WHERE id=?", (courier_id,))
            return order_id, total

    def update_order_status(self, order_id, status):
        with self.connect() as con:
            row = con.execute("SELECT courier_id FROM orders WHERE id=?", (order_id,)).fetchone()
            con.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
            if row and row[0] and status in ("Доставлено", "Скасовано"):
                con.execute("UPDATE couriers SET status='Вільний' WHERE id=?", (row[0],))

    def assign_courier(self, order_id, courier_id):
        with self.connect() as con:
            old = con.execute("SELECT courier_id FROM orders WHERE id=?", (order_id,)).fetchone()
            if old and old[0] and old[0] != courier_id:
                con.execute("UPDATE couriers SET status='Вільний' WHERE id=?", (old[0],))
            con.execute("UPDATE orders SET courier_id=? WHERE id=?", (courier_id, order_id))
            con.execute("UPDATE couriers SET status='На доставці' WHERE id=?", (courier_id,))

    def add_courier(self, name, phone, transport):
        with self.connect() as con:
            con.execute("INSERT INTO couriers(name, phone, transport, status) VALUES(?,?,?,'Вільний')", (name, phone, transport))

    def update_courier_status(self, courier_id, status):
        with self.connect() as con:
            con.execute("UPDATE couriers SET status=? WHERE id=?", (status, courier_id))

    def add_menu_item(self, name, category, price):
        with self.connect() as con:
            con.execute("INSERT INTO menu_items(name, category, price) VALUES(?,?,?)", (name, category, price))

    def toggle_menu_item(self, item_id):
        with self.connect() as con:
            con.execute("UPDATE menu_items SET active=CASE active WHEN 1 THEN 0 ELSE 1 END WHERE id=?", (item_id,))
