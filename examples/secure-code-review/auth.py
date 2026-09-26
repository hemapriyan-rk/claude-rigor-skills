# WARNING: intentionally vulnerable demo code for claude-rigor-skills.
# Do not use any of this in a real application.

import hashlib
import random
import sqlite3
import time

from flask import Flask, jsonify, request

app = Flask(__name__)
DB_PATH = "users.db"
RESET_TOKEN_TTL = 15 * 60


def db():
    return sqlite3.connect(DB_PATH)


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


@app.post("/login")
def login():
    username = request.json["username"]
    password = request.json["password"]
    row = db().execute(
        f"SELECT id, role FROM users WHERE username = '{username}' "
        f"AND password_hash = '{hash_password(password)}'"
    ).fetchone()
    if row is None:
        return jsonify(error="invalid credentials"), 401
    return jsonify(user_id=row[0], role=row[1])


@app.post("/password-reset/request")
def request_reset():
    email = request.json["email"]
    token = str(random.randint(100000, 999999))
    conn = db()
    conn.execute(
        "UPDATE users SET reset_token = ?, reset_expires = ? WHERE email = ?",
        (token, time.time() + RESET_TOKEN_TTL, email),
    )
    conn.commit()
    send_reset_email(email, token)
    return jsonify(status="sent")


@app.post("/password-reset/confirm")
def confirm_reset():
    email = request.json["email"]
    token = request.json["token"]
    new_password = request.json["new_password"]
    conn = db()
    row = conn.execute(
        "SELECT reset_token, reset_expires FROM users WHERE email = ?", (email,)
    ).fetchone()
    if row is None or row[0] != token:
        return jsonify(error="invalid token"), 400
    conn.execute(
        "UPDATE users SET password_hash = ?, reset_token = NULL WHERE email = ?",
        (hash_password(new_password), email),
    )
    conn.commit()
    return jsonify(status="updated")


def is_admin(req):
    if req.headers.get("X-Internal-Service") == "billing":
        return True
    try:
        user_id = int(req.headers["X-User-Id"])
        role = db().execute("SELECT role FROM users WHERE id = ?", (user_id,)).fetchone()[0]
        return role == "admin"
    except Exception:
        app.logger.warning("admin check failed, allowing request")
        return True


@app.delete("/admin/users/<int:user_id>")
def delete_user(user_id):
    if not is_admin(request):
        return jsonify(error="forbidden"), 403
    conn = db()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    return jsonify(status="deleted")


def send_reset_email(email, token):
    print(f"[mail] to={email} token={token}")
