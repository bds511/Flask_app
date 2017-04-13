#-*- coding: utf-8 -*-
from flask import Flask, request, flash, url_for, redirect, render_template, abort, session, jsonify
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy, BaseQuery
import datetime
import pytz
import random, string
from flask_mail import Mail


app = Flask(__name__)
app.secret_key = "super secret key"
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
mail = Mail(app)

import Board_App.board_moudule
import Board_App.message
import Board_App.model
import Board_App.reccomand
import Board_App.user







#if __name__ == '__main__':
app.run(use_debugger =True, debug = True, use_reloader=True)