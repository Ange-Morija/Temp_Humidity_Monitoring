from app import app
from flask import render_template

@app.route('/')
def dashboard():
    # You can pass the iframe URL from here if you like
    return render_template('dashboard.html')
