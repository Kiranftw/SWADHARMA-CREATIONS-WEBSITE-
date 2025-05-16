from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound

app = Flask(__name__)

# Google Sheets setup
SHEET_ID = "1QJ8Ou9hklp3Nj_sXRAh6VIXGDoSBkgvS1W_dQ-S3wuQ"
SHEET_NAME = "Form Submissions"

def get_or_create_worksheet(sheet, worksheet_name):
    try:
        return sheet.worksheet(worksheet_name)
    except WorksheetNotFound:
        # Create worksheet with default 100 rows and 20 cols
        return sheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

def write_to_sheet(data):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "gen-lang-client-0601538388-ec8d64d51534.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SHEET_ID)
    worksheet = get_or_create_worksheet(sheet, SHEET_NAME)
    worksheet.append_row(data)

@app.route("/", methods=["GET", "POST"])
def landing_page():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        try:
            write_to_sheet([name, email,subject, message])
        except Exception as e:
            print(f"Error writing to Google Sheets: {e}")

        return redirect(url_for("landing_page"))

    return render_template("Landingpage.html")

@app.route("/casestudy")
def case_study():
    return render_template("CantactUs.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
