import datetime
import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('мм у тебя уже тут есть акк, добро пожаловать', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('лол не вышло', category='error')
        else:
            flash('Тебя не существует', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('пока', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        date_join = datetime.datetime.now()
        new_name = request.form.get('newName')
        user = User.query.filter_by(email=email).first()

        if user:
            flash('ты уже здесь :|', category='error')
        elif len(email) < 4:
            flash('добавь букв в имейл', category='error')
        elif len(first_name) < 2:
            flash(f'спасибо, {first_name}, а теперь нормальное имя', category='error')
        elif password1 != password2:
            flash('плиз ты только что ввел прошлый пароль, куда уже неправильно', category='error')
        elif len(password1) < 7:
            flash('коротко как твоя жизнь', category='error')
        elif len(new_name) < 1:
            flash('коротко как твоя жизнь', category='error')
        elif new_name.lower() == first_name.lower():
            flash('ты такое имя уже писал/а', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'), date_join=date_join, new_name=new_name)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('как жаль, ты зарегался, придется добавить тебя в базу данных', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('aaaa stan lino', category='success')
        return redirect(url_for('views.home'))
    dat = (datetime.datetime.now() - current_user.date_join).days
    rang = ""
    if 0 <= dat < 15:
        rang = "нугу"
    elif 15 < dat < 31:
        rang = "мини стэн"
    elif 31 < dat < 180:
        rang = "полгода с лино-я"
    elif 180 < dat < 366:
        rang = "приспешник сундундо"
    else:
        rang = "слуга ли минхо"

    return render_template("profile.html", user=current_user, dat=dat, rang=rang)


@auth.route('/change', methods=['GET', 'POST'])
@login_required
def change():
