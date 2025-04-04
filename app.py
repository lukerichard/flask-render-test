#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import sys
import os

app = Flask(__name__)
app.debug = True

print("Current working directory:", os.getcwd())
print("Python path:", sys.path)
print("Flask app instance path:", app.instance_path)

@app.route('/')
def home():
    try:
        return render_template('landing.html')
    except Exception as e:
        print("Error rendering template:", str(e))
        return str(e)

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(debug=True, port=5000) 