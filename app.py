#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired, Email, Length

from model import Pool, db_session
from sqlalchemy import or_


# ----------------------------------------------------------- flask configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'


# ----------------------------------------------------------- forms
class RegistrationForm(Form):
    "form object representing registration form"

    name = StringField('Name: ', validators=[InputRequired(), Length(min=3, max=60, message='Name must be at least %(min)d and at most %(max)d characters long')])
    email = StringField('Email: ', validators=[InputRequired(), Email(), Length(max=120, message='Email is too long! At most %(max)d characters allowed!')])
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
        # verify if the same data already exists in database
        participant = db_session.query(Pool).filter(or_(Pool.name==form.name.data, Pool.email==form.email.data)).first()
        if participant:
            flash('The name or email you gave already exists; please use another name or email.')
            return redirect(url_for('register'))

        # do a db write
        player = Pool(name=form.name.data, email=form.email.data, confirmed=False, winner=False)
        db_session.add(player)
        db_session.commit()

        # store user session
        session['name'] = form.name.data

        # redirect to confirmation page
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
