from flask import Flask, request, flash, url_for, redirect, render_template, abort, session, jsonify
import random, string
from Board_App import app
from .model import *
from werkzeug.security import generate_password_hash, check_password_hash




##로그인-------------



@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if user.query.filter(user.id==request.form['id']).first():
            User = user.query.filter(user.id==request.form['id']).one()
            if check_password_hash(User.password, request.form['password']):
                session['user_num'] = User.user_num
                session['nick_name'] = User.nick_name
        else:
            flash("아이디 혹은 비밀번호가 잘못되었습니다.")
            return redirect(request.referrer)
        return redirect(request.referrer)
    return ''

@app.route('/user/join', methods=['GET', 'POST'])
def join():
    error=None
    if request.method== 'POST':
        if user.query.filter(user.id==request.form['join_id']).first():
            flash("중복아이디.")
            return redirect(request.referrer)
        else:
            add_to_user = user(request.form['join_id'], request.form['join_password'], request.form['nick_name'], request.form['email'])
            db.session.add(add_to_user)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("join.html", error=error)


@app.route('/user/logout')
def logout():
    session.pop('user_num', None)
    session.pop('nick_name', None)
    return redirect(url_for('home'))

@app.route('/user/user_info/<int:number>')
def user_info(number):
    User=user.query.get(number)
    return render_template("user_info.html", User=User)



@app.route('/id_checker')
def id_checker():
    a=request.args.get('a')
    print(a)
    if user.query.filter(user.id==a).first():
        print("ass")
        return jsonify(id_checking="ID중복")
    else:
        return jsonify(id_checking="만들 수 있는 ID")



##로그인 끝

