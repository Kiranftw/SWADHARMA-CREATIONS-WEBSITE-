SWADHARMA Creations Website – Contact Form Integration
This repository contains the source code for the SWADHARMA Creations website, built with Flask. The website includes:
A contact form that writes client details to Google Sheets
Automatic email notifications sent to the business inbox
A database logger for monitoring submissions and system activity

✨ Features

Contact Form: Clients can submit their details (Name, Email, Subject, Message).
Google Sheets Integration: Every submission is appended to a Google Sheet for easy access.
Email Notification: Business owners automatically receive an email with form details.
Database Logging: Submissions and system logs (SUCCESS/FAILURE) are stored in a database for monitoring.
Secure Configuration: Sensitive keys and credentials are stored in a .env file and not committed to GitHub.

🔑 Prerequisites

Python 3.10+
A Google Cloud Project
A Google Sheets document created and shared with your Service Account email
A Gmail account with App Passwords enabled (required for sending emails)

🛠 Setup Instructions
1. Clone this repository
git clone https://github.com/yourusername/swadharma-creations.git
cd swadharma-creations

2. Create a Google Cloud Service Account
Go to Google Cloud Console
.
Create a new project (example: swadharma-contactform).
Enable the Google Sheets API and Google Drive API.
Go to IAM & Admin → Service Accounts.
Create a new service account.
Download the JSON key file (this is your credentials file).
Share your Google Sheet with the service account email (looks like:
your-service@your-project.iam.gserviceaccount.com) with Editor access.

3. Configure Environment Variables
Create a .env file in your project root:

SECRET_KEY=your_secret_key
SHEET_ID=your_google_sheet_id
SHEET_NAME="CLIENT's DETAILS"
GOOGLE_APPLICATION_CREDENTIALS=swadharma-contactform.json
YOUR_EMAIL=yourbusiness@gmail.com
APP_PASSWORD=your_app_password_here
DATABASE_URL=sqlite:///contactform.db

⚠️ Never commit .env or your JSON key file to GitHub. Add them to .gitignore.
4. Install Dependencies
pip install -r requirements.txt
5. Run the Application
python app.py

The app will run locally at:
👉 http://127.0.0.1:5000

📊 Database & Logging

Submissions are stored in Google Sheets.
Logs and events are stored in a SQLite database (contactform.db).
Each log contains: timestamp, client details, status (SUCCESS/FAILURE), action performed (SHEET UPDATE, EMAIL SENT).

🔒 Security Notes

Keep this repo private for business use.
Do not share your .env file or JSON key.
Always use App Passwords for Gmail (never your actual password).
Rotate credentials periodically.

🚀 Future Enhancements

Admin dashboard to view submissions directly in the website
Migration to a production-ready database (PostgreSQL/MySQL)
Deployment on a cloud platform (Heroku, Render, GCP, or AWS)

✅ With this setup:

You have a Google Sheets backup (easy to share with clients).
You have emails for notifications.
You have a database for analytics & monitoring.