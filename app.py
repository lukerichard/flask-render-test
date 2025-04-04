#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__)
app.config['DEBUG'] = False  # Disable debug mode in production

@app.route('/')
def home():
    return render_template('landing.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) 