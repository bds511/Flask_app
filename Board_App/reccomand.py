from flask import Flask, request, flash, url_for, redirect, render_template, abort, session, jsonify

from Board_App import app
from .model import *




@app.route('/good/<int:number>')
def good(number):
    Contents = posting.query.get(number)
    if rec.query.filter(rec.user_num==session['user_num'], rec.number== number).first():
        st_to_good=rec.query.filter(rec.user_num == session['user_num'], rec.number == number).first()
        if st_to_good.good == False:
            st_to_good.good = True
            st_to_good.bad = False
            Contents.good +=1
            Contents.bad -=1
    else:
        Contents.good += 1
        Rec=rec(number, True,False)
        db.session.add(Rec)

    if Contents.good- Contents.bad > 30:
        Contents.board_num = 0
    db.session.commit()
    return jsonify(result=Contents.good, results=Contents.bad)

@app.route('/bad/<int:number>')
def bad(number):
    Contents = posting.query.get(number)
    if session['user_num']:

        if rec.query.filter(rec.user_num==session['user_num'], rec.number== number).first():
            st_to_good=rec.query.filter(rec.user_num == session['user_num'], rec.number == number).first()
            if st_to_good.good == True:
                st_to_good.good = False
                st_to_good.bad = True
                Contents.good -=1
                Contents.bad +=1
        else:
            Contents.bad += 1
            Rec=rec(number, False, True)
            db.session.add(Rec)
    db.session.commit()
    return jsonify(result=Contents.good, results=Contents.bad)





