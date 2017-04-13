import datetime
from flask import session, request, render_template, redirect, url_for
from Board_App import app
from .model import *
from flask_mail import Mail, Message
mail=Mail(app)



#메시지 보내기
@app.route('/send_message/<int:number>', methods=['GET', 'POST'])
def send_message(number):
    if session:
        if request.method == 'POST':
            msg_to_send=messenger(number, session['user_num'], user.query.get(number).nick_name, session['nick_name'], request.form['mess_title'], request.form['mess_body'])
            db.session.add(msg_to_send)
            db.session.commit()
            return redirect(url_for('message_index', number=1))
        else:
            nick_name = user.query.get(number).nick_name
            return render_template("send_message.html", nick_name=nick_name)
    else:
        return "로그인부터해주세요"


#메시지 읽기
@app.route('/read_message/<int:number>')
def read_message(number):
    if session:
        msg_to_read=messenger.query.get(number)
        print(session['user_num'] == msg_to_read.to_whom)
        if session['user_num'] == msg_to_read.to_whom or session['user_num'] == msg_to_read.by_whom:
            print("yes")
            if session['user_num'] == msg_to_read.to_whom:
                msg_to_read.read= True
                db.session.commit()

            return render_template('read_message.html', msg=msg_to_read, to_whom= user.query.get(msg_to_read.to_whom).nick_name, by_whom = user.query.get(msg_to_read.by_whom).nick_name)
        else:
            return '남의 쪽지는 볼 수 없어요'
    else:
        return "로그인부터해주세요"


#메시지 인덱스
@app.route('/message_index/<int:number>')
def message_index(number):
    if number==0:
        msg_to_read=messenger.query.filter(messenger.to_whom==session['user_num']).order_by(messenger.mess_num.desc()) #receiver
    if number==1:
        msg_to_read=messenger.query.filter(messenger.by_whom==session['user_num']).order_by(messenger.mess_num.desc()) #sender
    return render_template('message_index.html', msg_to_read=msg_to_read, number=number)


@app.route("/mail_sending")
def mail_sending():
	msg = Message(
              'Hello',
	       sender='postmaster@sandboxea99f9b0b00c476583bcd4ab4ef0925c.mailgun.org',
	       recipients=
               ['pypy7000@korea.ac.kr'])
	msg.body = "This is the email body"
	mail.send(msg)
	return "Sent"
