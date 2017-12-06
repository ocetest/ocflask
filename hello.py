#!/usr/bin/env python
#coding=utf-8
'''
Flask-WTF能保护所有表单免受跨站请求伪造的攻击
'''
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
#app.config字典可用来存储框架，扩展和程序本身的配置变量。
#SECRET_KEY配置变量是通用密钥，可以FLASK和多个第三方扩展中使用。
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
#Moment()用来同步系统时间
moment = Moment(app)

#这个表单中的字段都定义为类变量，类变量的值是相应字段类型的对象
#name为文本字段，submit为提交按钮
#StringField构造函数中的可选参数validators指定一个由验证函数组成的列表，在接受用户提交的数据之前
#验证数据
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators = [DataRequired()])
    submit = SubmitField('submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('505.html'), 505
'''
局部变量Name保存在用户会话中
包含合法表单数据的请求最后会调用redirect()函数，用来生成http重定向响应
url_for()生成URL，这个函数使用URL映射生成 URL
'''
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
