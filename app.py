#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired, Email, Length

# ----------------------------------------------------------- flask configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


# ----------------------------------------------------------- forms
class RegistrationForm(Form):
    "form object representing registration form"

    name = StringField('Name: ', validators=[InputRequired(), Length(min=3, max=60, message='Name must be at least %(min)d and at most %(max)d characters long')])
    email = StringField('Email: ', validators=[InputRequired(), Email()])
    submit = SubmitField('Submit')


# ----------------------------------------------------------- request handlers
@app.route('/')
def index():
    "home page handler"

    return render_template('index.html', title='Little Lottery')

@app.route('/register', methods=['GET', 'POST'])
def register():
    "register form handler"

    form = RegistrationForm()
    if form.validate_on_submit():
        # TODO: check if same data already exists in DB
        # TODO: write to database
        # store user session
        session['name'] = form.name.data
        return redirect(url_for('confirmation'))
    return render_template('register.html', title='Registration', form=form)

@app.route('/confirm')
def confirmation():
    "confirmation page handler"

    # if registration did not happen, user shouldn't be on this page
    if not session['name']:
        return redirect(url_for('index'))

    return render_template('confirmation.html', title='Confirmation', name=session['name'])

@app.route('/result')
def result():
    "lottery result page handler"

    return render_template('result.html', title='Result')

# ----------------------------------------------------------- app main entry
if __name__ == '__main__':
    app.run(debug=True)
