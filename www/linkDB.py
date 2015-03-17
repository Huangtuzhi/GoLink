#!/usr/bin/python
#-*- coding:utf-8-*-
__author__ = 'Huangyi' 

import sqlite3, os
ids = 1

class LinkDB(object):
	def __init__(self):
		self.db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'link.db')
		self.conn = sqlite3.connect(self.db_path)
		self.cursor = self.conn.cursor()

	def createDB(self):
		self.cursor.execute('''create table IF NOT EXISTS userinfo(userid INTEGER PRIMARY KEY, name text, password text)''')
		self.cursor.execute('''create table IF NOT EXISTS userlink(linkid INTEGER, userid INTEGER)''')
		self.cursor.execute('''create table IF NOT EXISTS linkinfo(linkid INTEGER, linkname text, path text, tag text)''')
		self.cursor.execute('''create unique index  IF NOT EXISTS userinfo_unique_index on userinfo(name)''')
		self.cursor.execute('''create unique index  IF NOT EXISTS userlink_unique_index on userlink(linkid)''')
		self.cursor.execute('''create unique index  IF NOT EXISTS linkinfo_unique_index on linkinfo(linkid)''')
		self.conn.commit()

	def insert_userinfo(self, name, password):
		name = name.strip().encode('utf-8') 
		password = password.strip().encode('utf-8')
		info = name, password
		try:
			self.cursor.execute('INSERT INTO userinfo(name, password) VALUES(?, ?)', info)
			self.conn.commit()
			return True
		except:
			return False
    
    #验证用户登陆
	def has_user(self, name, password):
		name = name.strip().encode('utf-8') 
		password = password.strip().encode('utf-8')
		info = name, password
		flag = self.cursor.execute('SELECT * FROM userinfo WHERE name=? and password=?', info).fetchall()
		if flag == []:
			return False
		else:
			return True

	def get_all_user_info(self):
		users = []
		rows = self.cursor.execute('SELECT userid, name, password FROM userinfo')
		for row in rows:
			users.append({'userid': row[0],
				          'name': row[1],
				          'password': row[2]
				          })
		return users

	def add_link(self, username, name, path, tag):
		global ids
		try:
			#不同的用户，ids都会增加
			#加链接有时候会出错，是不是全局变量ids的问题？使用事务？
			userid = self.cursor.execute('SELECT userid FROM userinfo WHERE name=?', (username,)).fetchone()
			self.cursor.execute('INSERT INTO userlink(linkid, userid) VALUES (?, ?)', (ids, userid[0]))
			ids += 1
			linkid = ids -1
			self.cursor.execute('INSERT INTO linkinfo(linkid, linkname, path, tag) VALUES (?, ?, ?, ?)', (linkid, name, path, tag))
			self.conn.commit()
			return True
		except:
			return False	
	
	def get_linkinfo_by_username(self, name):
		links = []
		userid = self.cursor.execute('SELECT userid FROM userinfo WHERE name=?', (name,)).fetchone()
		linkid = self.cursor.execute('SELECT linkid FROM userlink WHERE userid=?', userid).fetchall()
		for link in linkid:
			if link is not None:
				r = self.cursor.execute('SELECT linkid, linkname, path, tag FROM linkinfo WHERE linkid=?', link).fetchone()
				if r is not None:
					links.append({'linkid': r[0],
				          'linkname': r[1].encode('utf-8'),
				          'path': r[2].encode('utf-8'),
				          'tag': r[3].encode('utf-8')
				          })
		return links


if __name__ == '__main__':
	db = LinkDB()
	db.createDB()
	flag = db.insert_userinfo('huangyi', '123456')
	#flag3 = db.insert_userinfo('huangyi1', '1234561')
	#flag2 = db.add_link('huangyi1')
	#flag2 = db.add_link('huangyi','home', 'tuzhi.com', 'CS')
	#flag2 = db.add_link('huangyi','home1', 'tuzhi1.com', 'CS')
	#flag3 = db.add_link('huangyi','home1', 'tuzhi1.com', 'CS')
	flag3 = db.get_linkinfo_by_username('huangyi')



