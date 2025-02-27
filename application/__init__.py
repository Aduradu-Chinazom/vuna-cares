from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)

# Set a secret key for session management (required for using session)
app.secret_key =" config.SECRET_KEY"

from .route import *