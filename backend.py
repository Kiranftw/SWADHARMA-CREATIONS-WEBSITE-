from flask import Flask, request, redirect
import gspread
from google.oauth2.service_account import Credentials
from flask import render_template, url_for, flash

app = Flask(__name__)
app.secret_key = "super_secret_key_12345"

@app.before_request
def log_request_info():
    print("➡️ Method:", request.method)
    print("➡️ Path:", request.path)
    print("➡️ Form Data:", request.form)

@app.route("/")
def landing_page():
    return render_template("mainpage.html")

@app.route("/contactus", methods=["GET", "POST"])
def contactUS():
    if request.method == "POST":
        # Print EVERYTHING received in the POST request
        print("🔥 RAW POST DATA:", request.form)

        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        print("🔥 Received contact form submission:")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")

        flash("Your message has been sent successfully!", "success")
        return render_template("contactus.html", success=True)

    # For GET requests
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
    app.run(debug=True, port=5000)