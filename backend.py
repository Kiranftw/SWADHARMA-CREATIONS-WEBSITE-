from flask import Flask, request, render_template, flash, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import WorksheetNotFound
import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key_12345"

SHEET_ID = "10UNhMkGQkgRQlGgmQ7H5doN_sG7zJP8TxVQ21r63GVg"
SHEET_NAME = "SWDHARMACREATIONS"
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
        "gen-lang-client-0569515639-3d363533f5c5.json",
        scopes=scopes
    )
    client = gspread.authorize(credentials)

    sheet = client.open_by_key(SHEET_ID)
    worksheet = get_or_create_worksheet(sheet, SHEET_NAME)
    worksheet.append_row(data)

@app.before_request
def log_request_info():
    print("➡️ Method:", request.method)
    print("➡️ Path:", request.path)
    print("➡️ Form Data:", request.form)

@app.route("/")
def landing_page():
    return render_template("mainpage.html")

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(name, sender_email, subject, message):
    # Email account credentials
    YOUR_EMAIL = "udaykiranftw@gmail.com"
    APP_PASSWORD = "kjac hucn cbca azki"  # Use App Password, not your Gmail password

    # Create message
    msg = MIMEMultipart()
    msg['From'] = YOUR_EMAIL
    msg['To'] = YOUR_EMAIL  # Or any recipient you want
    msg['Subject'] = f"New Contact Form Submission: {subject}"

    body = f"Name: {name}\nEmail: {sender_email}\nSubject: {subject}\nMessage:\n{message}"
    msg.attach(MIMEText(body, 'plain'))

    # Connect to Gmail SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(YOUR_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ ERROR:", e)


@app.route("/contactus", methods=["GET", "POST"])
def contactUS():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        TIMESPAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("🔥 Contact form submission:")
        print(f"Name: {name}, Email: {email}, Subject: {subject}, Message: {message}")

        try:
            write_to_sheet([name, email, subject, message, TIMESPAMP])
            send_email(name, email, subject, message)
            print("✅ Data written to Google Sheets and email sent successfully!")
            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            print(f"❌ Error writing to Google Sheets: {e}")
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
    app.run(debug=True)
