from flask import Flask, request, render_template, flash
import gspread
from flask import url_for
from google.oauth2.service_account import Credentials
from gspread.exceptions import WorksheetNotFound
import datetime
import smtplib
import os
import sqlite3
import logging
from dotenv import load_dotenv, find_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

SHEET_ID = os.getenv("SHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
LOGGER = logging.getLogger()


def init_db():
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            name TEXT,
            email TEXT,
            subject TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()
    LOGGER.info("DATABASE INITIALIZED")


def save_to_db(timestamp, name, email, subject, message):
    conn = sqlite3.connect("contacts.db")
    c = conn.cursor()
    c.execute("INSERT INTO contacts (timestamp, name, email, subject, message) VALUES (?, ?, ?, ?, ?)",
              (timestamp, name, email, subject, message))
    conn.commit()
    conn.close()
    LOGGER.info(" DATA SAVED TO SQLITE DB")


def get_or_create_worksheet(sheet, worksheet_name):
    try:
        return sheet.worksheet(worksheet_name)
    except WorksheetNotFound:
        return sheet.add_worksheet(title=worksheet_name, rows="100", cols="20")


def write_to_sheet(data):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=scopes
    )
    client = gspread.authorize(credentials)

    sheet = client.open_by_key(SHEET_ID)
    worksheet = get_or_create_worksheet(sheet, SHEET_NAME)
    worksheet.append_row(data)
    LOGGER.info("DATA WRITTEN TO GOOGLE SHEETS")


def send_email(name, sender_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = YOUR_EMAIL
    msg['To'] = YOUR_EMAIL
    msg['Subject'] = f"New Contact Form Submission: {subject}"

    body = f"Name: {name}\nEmail: {sender_email}\nSubject: {subject}\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(YOUR_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        LOGGER.info("EMAIL SENT SUCCESSFULLY")
    except Exception as e:
        LOGGER.error(f"❌ EMAIL ERROR: {e}")

# ------------------ ROUTES ------------------


@app.before_request
def log_request_info():
    LOGGER.info(
        f"➡️ REQUEST | METHOD: {request.method} | PATH: {request.path} | FORM: {dict(request.form)}")


@app.route("/")
def landing_page():
    return render_template("mainpage.html")


@app.route("/contactus", methods=["GET", "POST"])
def contactUS():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        LOGGER.info(
            f"🔥 CONTACT FORM SUBMISSION | Name: {name}, Email: {email}, Subject: {subject}")

        try:
            write_to_sheet([timestamp, name, email, subject, message])
            save_to_db(timestamp, name, email, subject, message)
            send_email(name, email, subject, message)

            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            LOGGER.error(f"❌ ERROR HANDLING CONTACT FORM: {e}")
            flash("Something went wrong. Please try again later.", "error")

        return render_template("contactus.html", success=True)

    return render_template("contactus.html")


@app.route("/aboutus")
def aboutUS():
    return render_template("aboutus.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/workpage")
def workpage():
    return render_template("workpage.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)