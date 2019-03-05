from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = "thisisnotasecretkey"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_email():
    mysql = connectToMySQL("email_validation")
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Email is not valid!")  
    query = "SELECT email FROM email_table WHERE EXISTS (SELECT email FROM email_table WHERE email=%(em)s);"
    data = {
        "em": request.form['email']
    }
    if mysql.query_db(query, data):
        flash("Email is not valid!")

    if not '_flashes' in session.keys():    
        query = "INSERT INTO email_table (email, created_at) VALUES (%(em)s, NOW());"
        mysql.query_db(query, data)
        flash("Congrats you entered a valid email!")
        return redirect("/success")
    return redirect('/')

@app.route('/success')
def success_doc():
    mysql = connectToMySQL("email_validation")
    emails = mysql.query_db("SELECT * FROM email_table;")
    print(emails)
    for email in emails:
        print(email['email'])
    return render_template("emails.html", emails=emails)

if __name__ == "__main__":
    app.run(debug=True)