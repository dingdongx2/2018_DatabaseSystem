from flask import Flask, redirect, request, render_template, session, url_for
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/order", methods=["POST"])
def order():
    # error
    if not request.form.get("name") or not request.form.get("cafeteria"):
        return render_template("failure.html")

    file = open("order.csv", "a", newline="", encoding="utf-8")
    writer = csv.writer(file)
    writer.writerow((request.form.get("name"), request.form.get("cafeteria")))
    file.close()

    return render_template("success.html")

# export FLASK_APP=app
# flask run
