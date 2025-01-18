from flask import Flask,redirect,url_for,render_template,request
from application import app
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
    return render_template('index.html')
 
@app.route("/view_more")
def view_more():
    return render_template('view_more.html')

@app.route("/success")
def success():
    return render_template('success.html')
