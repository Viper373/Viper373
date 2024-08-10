from flask import Flask, redirect, request, render_template, session, flash, send_from_directory
import os
from datetime import timedelta
import pymysql
import re

app = Flask(__name__, template_folder='templates')
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 配置7天有效


# 查询语句，返回一个结果集
def select_sql(sql_string):
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='clock', port=3306, charset='utf8')
    cursor = conn.cursor()
    cursor.execute(sql_string)
    conn.close()
    data_all = cursor.fetchall()
    return data_all


# 删除、插入、修改语句，执行完毕返回True
def other_sql(sql_string):
    conn = pymysql.connect(host='localhost', user='root', password='123456', db='clock', port=3306, charset='utf8')
    cursor = conn.cursor()
    cursor.execute(sql_string)
    conn.commit()
    conn.close()
    return True


# 判断是否有session，session是否为管理员账户，正确返回True，错误返回False
def get_session():
    boolean = False
    userID = session.get('userID')
    if userID is not None:
        result = select_sql("select userID from admin where userID = \'{}\'".format(userID))
        if len(result) != 0:
            boolean = True
    return boolean


@app.route('/clear_session', methods=['GET', 'POST'])
def clear():
    if get_session() is True:
        session.clear()  # 清除所有session
        flash('退出成功！')
        return redirect("login.html")
    else:
        flash('您还没有登录！')
        return redirect("login.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), '../../lpl.viper3.top/static/favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# 首页
@app.route('/', methods=['GET', 'POST'])
def Index():
    return render_template('index.html')


# 登录
@app.route("/login.html", methods=['GET', 'POST'])
def Login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        userID = request.form.get("userID")
        password = request.form.get("password")
        # 进行有无特殊字符判断，防止sql注入(正则匹配特殊字符，没有特殊字符则返回None)
        Special_characters_userID = re.search(r"\W", userID)
        Special_characters_password = re.search(r"\W", password)
        if Special_characters_userID is None and Special_characters_password is None:
            # 进行账号密码验证
            result = select_sql(
                "select * from admin where userID = \'{}\' and password = \'{}\'".format(userID, password))
            if len(result) != 0:
                session['userID'] = userID  # 设置“字典”键值对
                session.permanent = True  # 设置session的有效时间，长期有效，一个月的时间有效，具体看上面的配置时间具体的，没有上面设置的时间就是一个月有效
                return redirect("UserInfo.html")
            else:
                flash('用户名或密码错误，请重试！')
                return redirect("login.html")
        else:
            flash('请勿输入特殊字符！')
            return redirect("login.html")


# 用户信息页面
@app.route('/UserInfo.html', methods=['GET', 'POST'])
def UserInfo():
    if get_session() is True:
        data_all = select_sql("select * from user")
        data_all = list(data_all)
        return render_template('UserInfo.html', data_all=data_all, num=len(data_all))
    else:
        flash("请先进行登录! ")
        return redirect("login.html")


# 查询某个用户信息
@app.route('/Select', methods=['GET', 'POST'])
def Select():
    if get_session() is True:
        if request.method == 'GET':
            return redirect("Userinfo.html")
        if request.method == 'POST':
            Select_key = request.form.get("Select_key")
            Select_value = request.form.get("Select_value")
            if Select_key == "*" or Select_value == "":
                return redirect("UserInfo.html")
            else:
                data = select_sql("select * from user where {} = \'{}\'".format(Select_key, Select_value))
                data = list(data)
                return render_template('UserInfo.html', data_all=data, num=len(data))
    else:
        flash("请先进行登录! ")
        return redirect("login.html")


# 删除某个用户
@app.route('/Delete', methods=['GET', 'POST'])
def Delete():
    if get_session() is True:
        if request.method == 'GET':
            return redirect("UserInfo.html")
        if request.method == 'POST':
            array_userID = request.values.getlist("array_userID")
            if len(array_userID) == 0:
                flash("没有选择用户或者该用户不可编辑！")
                return redirect("UserInfo.html")
            for userID in array_userID:
                other_sql("delete from user where userID = \'{}\'".format(userID))
            flash("删除完成！")
        return redirect("UserInfo.html")
    else:
        flash("请先进行登录! ")
        return redirect("login.html")


# 修改 某个用户的数据 的页面
@app.route('/UpData_Page.html', methods=['GET', 'POST'])
def UpData_Page():
    if get_session() is True:
        userID = request.values.get("userID")
        print(userID)
        oneUserInfo = select_sql("select * from user where userID = \'{}\'".format(userID))
        oneUserInfo = list(oneUserInfo)
        return render_template('UpData_Page.html', value=oneUserInfo[0])
    else:
        flash("请先进行登录! ")
        return redirect("login.html")


# 修改某个用户的数据
@app.route('/UpData', methods=['GET', 'POST'])
def UpData():
    if get_session() is True:
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
            boolean = other_sql(
                "update user set password=\'{}\', email=\'{}\', smtpServer=\'{}\', smtpSender=\'{}\', smtpPassword=\'{}\', expireDate=\'{}\' where userID=\'{}\'".format(
                    password, email, smtpServer, smtpSender, smtpPassword, expireDate, userID))
            if boolean:
                flash("已修改用户{}的信息".format(userID))
        return redirect("UserInfo.html")
    else:
        flash("请先进行登录! ")
        return redirect("login.html")


# 添加用户
@app.route('/Insert', methods=['GET', 'POST'])
def Insert():
    if get_session() is True:
        if request.method == 'GET':
            return render_template('newUser.html')
        if request.method == 'POST':
            userID = request.form.get("userID")
            result = select_sql("select userID from user where userID = \'{}\'".format(userID))
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
                # INSERT INTO table_name (列1, 列2,...) VALUES (值1, 值2,....)
                boolean = other_sql(
                    "INSERT INTO user (userID,password,email,smtpServer,smtpSender,smtpPassword,expireDate) "
                    "VALUES (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')"
                    .format(userID, password, email, smtpServer, smtpSender, smtpPassword, expireDate))
                if boolean:
                    flash("添加用户成功! ")
                return redirect("UserInfo.html")
    else:
        flash("请先进行登录! ")
        return redirect("login.html")


if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True)
