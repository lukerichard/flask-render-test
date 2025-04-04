#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import os

app = Flask(__name__)
app.debug = False  # Disable debug mode in production

@app.route('/')
def home():
    return render_template('landing.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port) 