#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    "home page handler"

    return render_template('index.html', title='Welcome')

@app.route('/register')
def register():
    "register form handler"

    return render_template('register.html', title='Registration')

@app.route('/confirm')
def confirmation():
    "confirmation page handler"

    return render_template('confirmation.html', title='Confirmation')

@app.route('/result')
def result():
    "lotter result page handler"

    return render_template('result.html', title='Result')

if __name__ == '__main__':
    app.run(debug=True)
