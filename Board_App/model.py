from Board_App import db
import datetime
from flask import session, g
from Board_App import app
from werkzeug.security import generate_password_hash, check_password_hash


#메신저 관련
class messenger(db.Model):
    __tablename__ =  'message'
    mess_num = db.Column(db.Integer, db.Sequence('message_mess_num_seq'), primary_key=True)
    to_whom= db.Column(db.Integer)
    by_whom = db.Column(db.Integer)
    to_whom_nick_name = db.Column(db.Text)
    by_whom_nick_name = db.Column(db.Text)
    mess_title=db.Column(db.Text)
    mess_body=db.Column(db.Text)
    send_date=db.Column(db.Date)
    read_date=db.Column(db.Date)
    read=db.Column(db.BOOLEAN)

    def __init__(self, to_whom=None, by_whom= None, to_whom_nick_name=None, by_whom_nick_name=None, mess_title=None, mess_body=None):
        self.to_whom=to_whom
        self.by_whom = by_whom
        self.to_whom_nick_name=to_whom_nick_name
        self.by_whom_nick_name=by_whom_nick_name
        self.mess_title = mess_title
        self.mess_body = mess_body
        self.send_date=datetime.date.today()
        self.read=False


#글관련
class posting(db.Model):
    __tablename__ = 'board'
    number = db.Column(db.Integer, db.Sequence('board_number_seq'), primary_key= True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    date = db.Column(db.Date)
    user_num = db.Column(db.Text)
    nick_name = db.Column(db.Text)
    hit = db.Column(db.Integer)
    good = db.Column(db.Integer)
    bad = db.Column(db.Integer)
    board_num=db.Column(db.Integer)

    def __init__(self, title=None, body=None, user_num = None, nick_name= None, board_num=None ):
        self.title = title
        self.body = body
        self.date = datetime.date.today()
        self.user_num = user_num
        self.nick_name = nick_name
        self.hit = 0
        self.good = 0
        self.bad = 0
        self.board_num=board_num

class board_list(db.Model):
    __tablename__= 'board_list'
    board_num=db.Column(db.Integer, db.Sequence('board_list_board_num_seq'), primary_key=True)
    board_name = db.Column(db.Text)

    def __init__(self, board_name=None):
        self.boad_name=board_name




#추천관련
class rec(db.Model):
    __tablename__ = 'rec_board'
    user_num= db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, primary_key=True)
    good=db.Column(db.BOOLEAN)
    bad=db.Column(db.BOOLEAN)

    def __init__(self, number, good, bad):
        self.user_num= session['user_num']
        self.number= number
        self.good= good
        self.bad = bad

# 코멘트 관련
class commentor(db.Model):
    __tablename__ = 'comments'
    number = db.Column(db.Integer)
    comment_num = db.Column(db.Integer, db.Sequence('comments_comment_num_seq'), primary_key= True)
    comment = db.Column(db.Text)
    date = db.Column(db.Date)
    user_num = db.Column(db.Text)
    nick_name = db.Column(db.Text)
    parent_comment_num= db.Column(db.Integer)


    def __init__(self, number=None, comment=None, user_num = None, nick_name= None, parent_comment_num=None):
        self.number = number
        self.comment = comment
        self.date = datetime.date.today()
        self.user_num = user_num
        self.nick_name = nick_name
        self.parent_comment_num= parent_comment_num




#유저관련
class user(db.Model):
    __tablename__ =  'User'
    id= db.Column(db.Text)
    password = db.Column(db.Text)
    nick_name=db.Column(db.Text)
    email=db.Column(db.Text)
    user_num = db.Column(db.Integer, db.Sequence('User_user_num_seq'), primary_key=True)


    def __init__(self, id = None, password= None, nick_name =None, email= None):
        self.id=id
        self.password = generate_password_hash(password)
        self.nick_name = nick_name
        self.email = email




@app.context_processor
def inject_board_list():
    return dict(g_board_list=board_list.query.order_by(board_list.board_num.asc()))