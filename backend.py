import flask
from flask import render_template, Flask
app = Flask(__name__)

@app.route("/")
def landing_page():
    return render_template("Landingpage.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)