from flask import Flask, request, flash, url_for, redirect, render_template, abort, session, jsonify
from sqlalchemy import or_
from Board_App import app
from .model import *


##인덱스
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/board', methods=["GET", "POST"])
def index():
    if request.args.get('page'): ##페이지선택
        number=int(request.args.get('page'))
    else:
        number=1

    if request.args.get('board_num'): #게시판 선택
        board_num=request.args.get('board_num')
        print(board_num)
    else:
        board_num=2


    if request.args.get('search_type'): ##검색
        search_type=request.args.get('search_type')
        if search_type == "title":
            Contents = posting.query.filter(posting.board_num==board_num, posting.title.like('%' + str(request.args.get('q')) + "%")).order_by(
                posting.number.desc())
        if search_type == "body":
            Contents= posting.query.filter(posting.board_num==board_num, posting.body.like('%' + str(request.args.get('q')) + "%")).order_by(posting.number.desc())
        if search_type == "title_body":
            Contents = posting.query.filter(posting.board_num==board_num,
                or_(posting.body.like('%' + str(request.args.get('q')) + "%"),
                    posting.body.like('%' + str(request.args.get('q')) + "%"))).order_by(
                posting.number.desc())
        if search_type == "nick_name":
            Contents = posting.query.filter(posting.board_num==board_num,
                posting.nick_name.like('%' + str(request.args.get('q')) + "%")).order_by(
                posting.number.desc())
    else:
        Contents = posting.query.filter(posting.board_num == board_num).order_by(posting.number.desc())

    last_num = round((Contents.count()/15)+0.5) ## 인덱스 계산
    if last_num < number:
        number=last_num
    min_num= max(number-5,1)
    max_num= min(last_num, min_num+10)

    if request.args.get('mode') in ["view", "commenting", "del_comment", "fix"]: ##특정글위에서만 이뤄지는것들
        if request.args.get('view_number'):
            view_number=request.args.get('view_number')
            view_contents = posting.query.get(view_number)
            if request.args.get('mode') == "view": ##보기
                view_contents.hit += 1
                db.session.commit()

            if request.args.get('mode')== "commenting": ##댓글달기
                Comment = commentor(view_number, request.form['comment'], session['user_num'], session['nick_name'], request.form['parent_comment_num'])
                db.session.add(Comment)
                db.session.commit()

            if request.args.get('mode')== "del_comment": # 댓글삭제
                comment_num=int(request.args.get('comment_num'))
                Comment = commentor.query.get(comment_num)
                if session['user_num'] == Comment.user_num:
                    Comment.comment="삭제된 메시지"
                    db.session.commit()

            if request.args.get('mode') == "fix": ## 수정
                if view_contents.user_num == session['user_num']:
                    if request.method == "GET":
                        return render_template("fix.html", contents=view_contents, view_contents= view_contents, **request.args)
                    view_contents.title = request.form['title']
                    view_contents.body = request.form['body']
                    view_contents.nick_name = session['nick_name']
                    db.session.commit()
                else:
                    return "게시물 작성자만 수정 가능합니다."

            Comments = commentor.query.filter(commentor.number == view_number).all()
            return render_template("view.html", **request.args, board_num=board_num, view_contents= view_contents, comments=Comments, contents=Contents[(number-1)*15 : number*15], number=number, min_num=min_num, max_num=max_num, last_num=last_num,)

    if request.args.get('mode') == "delete": ##삭제
        view_number=request.args.get("view_number")
        st_to_del = posting.query.get(view_number)
        if st_to_del.user_num == session['user_num']:
            db.session.delete(st_to_del)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            return '게시물 작성자만 삭제가능합니다.'
    if request.args.get('mode')== 'posting':
        if session.get('user_num'):
            if request.method == 'POST':
                add_to_db = posting(request.form['title'],  request.form['body'], session['user_num'], session['nick_name'])
                db.session.add(add_to_db)
                db.session.commit()
                return redirect(url_for('index'))
            return render_template('new.html', mode="posting")
        return "로그인먼저 해주세요"

    return render_template('index.html', contents=Contents[(number - 1) * 15: number * 15], number=number,
                               min_num=min_num, max_num=max_num, last_num=last_num, **request.args)

@app.route('/board/write', methods=["GET", "POST"])
def write():
    if session.get('user_num'):
        if request.method == 'POST':
            add_to_db = posting(request.form['title'],  request.form['body'], session['user_num'], session['nick_name'], request.form['board_num'])
            db.session.add(add_to_db)
            db.session.commit()
            return redirect(url_for('index', board_num= request.form['board_num']))
        return render_template('new.html')
    return "로그인먼저 해주세요"



#인덱스 끝
