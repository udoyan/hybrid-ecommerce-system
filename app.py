from flask import Flask, render_template, request
import psycopg2
from pymongo import MongoClient
from datetime import datetime

# 🔹 Import config
from config import POSTGRES_CONFIG, MONGO_URI, MONGO_DB

app = Flask(__name__)

# =========================
# DATABASE CONNECTIONS
# =========================

pg_conn = psycopg2.connect(**POSTGRES_CONFIG)
pg_cursor = pg_conn.cursor()

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB]

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# ADD PRODUCT
@app.route("/add_product", methods=["POST"])
def add_product():
    name = request.form["name"]
    price = float(request.form["price"])
    stock = int(request.form["stock"])
    category = request.form["category"]
    description = request.form["description"]

    pg_cursor.execute(
        "INSERT INTO products (name, price, stock_quantity, category) VALUES (%s,%s,%s,%s) RETURNING id",
        (name, price, stock, category)
    )
    product_id = pg_cursor.fetchone()[0]
    pg_conn.commit()

    mongo_db.product_details.insert_one({
        "product_id": product_id,
        "description": description,
        "reviews": []
    })

    return f"<h3 style='color:green;'>✔ Product Added (ID: {product_id})</h3>"


# PLACE ORDER
@app.route("/place_order", methods=["POST"])
def place_order():
    user_id = int(request.form["user_id"])
    product_id = int(request.form["product_id"])
    quantity = int(request.form["quantity"])

    pg_cursor.execute(
        "SELECT stock_quantity, price FROM products WHERE id=%s",
        (product_id,)
    )
    result = pg_cursor.fetchone()

    if not result:
        return "<h3 style='color:red;'>Product not found</h3>"

    stock, price = result

    if stock < quantity:
        return "<h3 style='color:red;'>Not enough stock</h3>"

    pg_cursor.execute(
        "UPDATE products SET stock_quantity = stock_quantity - %s WHERE id=%s",
        (quantity, product_id)
    )

    total = price * quantity

    pg_cursor.execute(
        "INSERT INTO orders (user_id, total_amount, status) VALUES (%s,%s,%s) RETURNING id",
        (user_id, total, "PAID")
    )
    order_id = pg_cursor.fetchone()[0]

    pg_cursor.execute(
        "INSERT INTO order_items VALUES (%s,%s,%s,%s)",
        (order_id, product_id, quantity, price)
    )

    pg_conn.commit()

    mongo_db.activity_log.insert_one({
        "user_id": user_id,
        "actions": [{
            "type": "PLACE_ORDER",
            "product_id": product_id,
            "timestamp": datetime.utcnow()
        }]
    })

    return f"<h3 style='color:green;'>✔ Order placed (ID: {order_id})</h3>"


# VIEW PRODUCT
@app.route("/view_product", methods=["POST"])
def view_product():
    product_id = int(request.form["product_id"])

    pg_cursor.execute(
        "SELECT name, price, stock_quantity FROM products WHERE id=%s",
        (product_id,)
    )
    product = pg_cursor.fetchone()

    if not product:
        return "<h3 style='color:red;'>Product not found</h3>"

    details = mongo_db.product_details.find_one({"product_id": product_id})

    return f"""
    <div style='padding:20px;'>
        <h2>{product[0]}</h2>
        <p><b>Price:</b> {product[1]}</p>
        <p><b>Stock:</b> {product[2]}</p>
        <p><b>Description:</b> {details.get('description','')}</p>
    </div>
    """


# ADD REVIEW
@app.route("/add_review", methods=["POST"])
def add_review():
    product_id = int(request.form["product_id"])
    user_id = int(request.form["user_id"])
    rating = int(request.form["rating"])
    comment = request.form["comment"]

    mongo_db.product_details.update_one(
        {"product_id": product_id},
        {"$push": {
            "reviews": {
                "user_id": user_id,
                "rating": rating,
                "comment": comment
            }
        }}
    )

    return "<h3 style='color:green;'>✔ Review Added</h3>"


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)