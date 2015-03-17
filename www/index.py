#!/usr/bin env python
#-*- coding: utf-8 -*-
import sys
from flask import Flask, request, render_template, redirect, url_for, session
from linkDB import LinkDB
app = Flask(__name__)
app.secret_key = '\xf8y\x9573\x1b\x13X\xf8\x8eG=\x87\x8bh\xc7\xab\x9eqwF\xd2\xa5\xac'

reload(sys)
sys.setdefaultencoding('utf-8')

@app.route('/')
def web():
	if 'username' in session:
		return render_template('page.html')
	return render_template('signin.html')

#name和pasword在get和post方法中分别为空对象和空字符串
@app.route('/signin', methods=['GET', 'POST'])
def web_signin():
	if request.method == 'GET':
		return redirect(url_for('web'))
	if request.method == 'POST':
		name = request.form.get('username', None)
		session['username'] = name
		password = request.form.get('password', None)
		db = LinkDB()
		if name.strip()=='' or password.strip()=='':
			return redirect(url_for('web'))
		if db.has_user(name, password):
			return render_template('page.html') #返回用户页面 
		else:
			return '用户名或密码错误'


	
@app.route('/signup', methods=['GET', 'POST'])
def web_signup():
	name = request.form.get('username', None)
	password = request.form.get('password', None)
	if name is None or password is None: #get
		return render_template('signup.html')
	else: #post
		db = LinkDB()
		if name.strip()=='' or password.strip()=='':
			return render_template('signup.html')
		flag = db.insert_userinfo(name, password)	
		if flag == True:
			return redirect(url_for('web'))
		else:
			return '注册失败'

# 用户，及其信息列表
@app.route('/user', methods=['GET'])
def web_user():
	db = LinkDB()
	users = db.get_all_user_info()
	return render_template('homepage.html', users=users)

#用户添加link
@app.route('/addlink', methods=['GET', 'POST'])
def add_link():
	if request.method == 'GET':
		return render_template('add_link.html')
	if request.method == 'POST':
		db = LinkDB()
		name = request.form.get('name', None)
		path = request.form.get('path', None)
		tag = request.form.get('tag', None)
		#有时添加数据库会出错
		if db.add_link(session['username'], name, path, tag) is True:
			return redirect(url_for('web_link'))
		else:
			return '链接未添加'
	
#返回用户所有link	
@app.route('/link', methods=['GET'])
def web_link():
	db = LinkDB()
	links = db.get_linkinfo_by_username(session['username'])
	print links
	if links is None:
		return 'No links'
	return render_template('link.html', links=links)

@app.route('/logout', methods=['GET'])
def quit():
	session.pop('username', None)
	return render_template('signin.html')


if __name__ == '__main__':
	app.run(host='127.0.0.1', debug=True)