#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired, Email, Length

from sqlalchemy import or_, func
from sqlalchemy.orm.exc import NoResultFound

from model import Pool, db_session
from lottery import LittleLottery

# ----------------------------------------------------------- constants
FIVE_DAYS_IN_SECONDS = 5*24*60*60


# ----------------------------------------------------------- flask configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['WINNER'] = None
app.config['LOTTERY_OPEN_TIME'] = time.time() + FIVE_DAYS_IN_SECONDS


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

    return render_template('index.html', title='Little Lottery', open_lottery=app.config['WINNER'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    "register form handler"

    if app.config['WINNER']:
        return redirect(url_for('index'))

    form = RegistrationForm() 
    if form.validate_on_submit():
        # verify if the same data already exists in database
        participant = db_session.query(Pool).filter(or_(Pool.name==form.name.data, Pool.email==form.email.data)).first()
        if participant:
            flash('The name or email you gave already exists; please use another name or email.')
            return redirect(url_for('register'))

        # do a db write
        player = Pool(name=form.name.data, email=form.email.data)
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

    now = time.time()
    if (now - app.config['LOTTERY_OPEN_TIME']) >= 0:
        if not app.config['WINNER']:

            # check if winner already exists from database
            q = db_session.query(Pool).filter(Pool.winner==True)
            winner_exists = db_session.query(q.exists()).scalar()

            if winner_exists:
                app.config['WINNER'] = q.one()
                return render_template('result.html',
                                       title='Result',
                                       open_lottery=True,
                                       winner=app.config['WINNER'])

            # winner does not exist, run lottery algorithm to generate the winner
            pool_size = db_session.query(func.count(Pool.id)).scalar()
            lottery = LittleLottery(pool_size)
            try:
                w = db_session.query(Pool).filter(Pool.id==lottery.draw()).one()
            except NoResultFound as e:
                pass
            else:
                # winner created, now write to db
                w.winner = True
                db_session.commit()

                # cache it in app configuration
                app.config['WINNER'] = w
        return render_template('result.html',
                                title='Result',
                                open_lottery=True,
                                winner=app.config['WINNER'])

    open_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(app.config['LOTTERY_OPEN_TIME']))
    return render_template('result.html', title='Result', open_lottery=False, open_time=open_time)


# ----------------------------------------------------------- app main entry
if __name__ == '__main__':
    app.run(debug=True)
