import flask
from flask import render_template, Flask
app = Flask(__name__)

@app.route("/")
def landing_page():
    return render_template("Landingpage.html")

@app.route("/casestudy")
def case_study():
    return render_template("CantactUs.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)