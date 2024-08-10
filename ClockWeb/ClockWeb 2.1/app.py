from flask import Flask, redirect, request, render_template, session, flash, send_from_directory, jsonify
from flask_sqlalchemy import pagination, SQLAlchemy
import functools
from gevent import pywsgi
import os
from datetime import timedelta
import pymysql
import re

app = Flask(__name__, template_folder='templates')
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 配置7天有效

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/clock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    userID = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(32))
    email = db.Column(db.String(32))
    smtpServer = db.Column(db.String(32))
    smtpSender = db.Column(db.String(32))
    smtpPassword = db.Column(db.String(32))
    expireDate = db.Column(db.String(32))


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.String(32))
    password = db.Column(db.String(32))


# 登录判断装饰器
def login_check(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        # 从session获取用户信息，如果有，则用户已登录，否则没有登录
        userID = session.get('userID')
        # print("session userID:", userID)
        if not userID:
            flash('您还没有登录！')
            return redirect("../login.html")
        else:
            return func(*args, **kwargs)

    return inner


# 手动退出登录，清除session
@app.route('/clear_session', methods=['GET', 'POST'])
@login_check
def clear():
    session.clear()  # 清除所有session
    flash('退出成功！')
    return redirect("login.html")


# 页面标签小图标
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), '../../lpl.viper3.top/static/favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# 首页
@app.route('/', methods=['GET', 'POST'])
def Index():
    # 首页未完善，直接跳转到登录页
    # return render_template('index.html')
    return redirect("/login.html")


# 登录
@app.route("/login.html", methods=['GET', 'POST'])
def Login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        userID = request.form.get("userID")
        password = request.form.get("password")
        result = Admin.query.filter_by(userID=userID).first()
        if result is None:
            flash("{} 该用户没有注册".format(userID))
            return redirect("login.html")
        elif result.password == password:
            session['userID'] = userID  # 设置“字典”键值对
            session.permanent = True  # 设置session的有效时间，长期有效，一个月的时间有效，具体看上面的配置时间具体的，没有上面设置的时间就是一个月有效
            return redirect("UserInfo.html")
        else:
            flash('用户名或密码错误，请重试！')
            return redirect("login.html")


# 用户信息页面
@app.route('/UserInfo.html/', methods=['GET', 'POST'])
@login_check
def UserInfo():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    paginate = User.query.paginate(page=int(page), per_page=per_page, error_out=False)
    page_data = paginate.items
    return render_template('UserInfo.html', paginate=paginate, page_data=page_data)


# 查询某个用户信息
@app.route('/Select', methods=['GET', 'POST'])
@login_check
def Select():
    if request.method == 'GET':
        return redirect("Userinfo.html")
    if request.method == 'POST':
        Select_key = request.form.get("Select_key")
        Select_value = request.form.get("Select_value")
        if Select_key == "*" or Select_value == "":
            return redirect("UserInfo.html")
        else:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 5))
            if Select_key == "userID":
                paginate = User.query.order_by(User.userID).filter_by(userID=Select_value).paginate(page=int(page), per_page=per_page, error_out=False)
            elif Select_key == "email":
                paginate = User.query.order_by(User.userID).filter_by(email=Select_value).paginate(page=int(page), per_page=per_page, error_out=False)
            else:
                paginate = User.query.order_by(User.userID).filter_by(expireDate=Select_value).paginate(page=int(page), per_page=per_page, error_out=False)
            page_data = paginate.items
            return render_template('UserInfo.html', paginate=paginate, page_data=page_data)


# 删除某个用户
@app.route('/Delete', methods=['GET', 'POST'])
@login_check
def Delete():
    if request.method == 'GET':
        return redirect("UserInfo.html")
    if request.method == 'POST':
        array_userID = request.values.getlist("array_userID")
        if len(array_userID) == 0:
            flash("没有选择用户或者该用户不可编辑！")
            return redirect("UserInfo.html")
        for userID in array_userID:
            user = User.query.filter_by(userID=userID).first()
            db.session.delete(user)
            db.session.commit()
        flash("删除完成！")
    return redirect("UserInfo.html")


# 修改 某个用户的数据 的页面
@app.route('/UpData_Page.html', methods=['GET', 'POST'])
@login_check
def UpData_Page():
    userID = request.values.get("userID")
    oneUserInfo = User.query.filter_by(userID=userID).first()
    return render_template('UpData_Page.html', value=oneUserInfo)


# 修改某个用户的数据
@app.route('/UpData', methods=['GET', 'POST'])
@login_check
def UpData():
    if request.method == 'GET':
        return redirect("Userinfo.html")
    if request.method == 'POST':
        userID = request.args.get("userID")
        password = request.form.get("password")
        email = request.form.get("email")
        smtpServer = request.form.get("smtpServer")
        smtpSender = request.form.get("smtpSender")
        smtpPassword = request.form.get("smtpPassword")
        expireDate = request.form.get("expireDate")
        user = User.query.filter_by(userID=userID).first()
        user.password, user.email, user.expireDate = password, email, expireDate
        user.smtpServer, user.smtpSender, user.smtpPassword = smtpServer, smtpSender, smtpPassword
        db.session.commit()
        flash("已修改用户{}的信息".format(userID))
    return redirect("UserInfo.html")


# 添加用户
@app.route('/Insert', methods=['GET', 'POST'])
@login_check
def Insert():
    if request.method == 'GET':
        return render_template('newUser.html')
    if request.method == 'POST':
        userID = request.form.get("userID")
        result = User.query.filter_by(userID='{}'.format(userID)).all()
        if len(result) != 0:
            flash("已经存在该用户! ")
            return redirect("/Insert")
        else:
            password = request.form.get("password")
            email = request.form.get("email")
            smtpServer = request.form.get("smtpServer")
            smtpSender = request.form.get("smtpSender")
            smtpPassword = request.form.get("smtpPassword")
            expireDate = request.form.get("expireDate")
            if smtpServer == "" or smtpSender == "" or smtpPassword == "":
                smtpServer = "smtp.exmail.qq.com"
                smtpSender = "mysheep@mysheep.cc"
                smtpPassword = "Yangjiaji0323"
            Info = User(userID=userID, password=password, email=email, smtpServer=smtpServer, smtpSender=smtpSender,
                        smtpPassword=smtpPassword, expireDate=expireDate)
            db.session.add_all([Info])
            db.session.commit()
            flash("添加用户成功! ")
            return redirect("UserInfo.html")


if __name__ == '__main__':
    # 开发环境
    # app.run(port=80, host='127.0.0.1', debug=True)

    # 线上部署
    server = pywsgi.WSGIServer(('127.0.0.1', 80), app)
    server.serve_forever()
