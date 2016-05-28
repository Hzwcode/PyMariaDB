#!usr/bin/env python
#-*-coding:utf8-*-

import pymysql
import pymysql.cursors

class mydb:
	prolist = (u"title",u"author",u"pdate",u"pcompany",u"pagenum",u"tags",u"isbn")
	basesql = "select isbn,title,author,pdate,pcompany,pagenum,tags from publication where %s;"
	def __init__(self):
		self._conn = pymysql.connect(
			host='localhost',
			user='root',
			password='mariadb1359434736',
			db='lab4',
			charset='utf8',
			cursorclass=pymysql.cursors.DictCursor
		)

	def __del__(self):
		#self._conn.commit()
		self._conn.close()

	def commit(self):
		self._conn.commit()

	def issql(self,arg):
		return "%s"%(unicode(arg))

	def likesql(self, arg):
		return "%%%s%%"%(unicode(arg))

	def textSearch(self, pro, text, concret = False):
		texts = text.split(" ")
		base = "%s like" if concret == False else "%s ="
		sql = ""
		args = list()
		for s in texts:
			if not s:
				continue
			sql = "or " + sql + base%(pro) + " %s "
			args.append(self.likesql(s) if concret == False else self.issql(s))
		sql = "(%s)" %sql[2:]
		return (sql, args)

	def cpSearch(self,pro,dates):
		sql1,sql2,sql="","",None
		args=list()
		if len(dates) == 1:
			sql = " " + pro + " = %s"
			args.append(dates[0])
			sql = "(%s)" %sql
			return (sql,args)
		if dates[0].strip():
			sql1 = " " + pro +" > %s "
		if dates[1].strip():
			sql2 = " " + pro + " < %s "
		if sql1:
			sql = sql1
			args.append(dates[0])
		if sql2:
			sql = sql1 + " and " + sql2
			if not sql1:
				sql = sql[4:]
			args.append(dates[1])
		sql = "(%s)" %sql
		return (sql,args)

	def search(self,csql,args=None):
		sql = self.basesql % csql
		result = None
		with self._conn.cursor() as cur:
			cur.execute(sql,args)
			print sql,args
			print cur.mogrify(sql,args)
			result = cur.fetchall()
		return result

	def insert(self,args):
		sql = "insert into publication(isbn,title,author,pdate,pcompany,pagenum,tags) \
				values (%s,%s,%s,%s,%s,%s,%s);"
		try:
			with self._conn.cursor() as cur:
				print len(args)
				print cur.mogrify(sql,args)
				cur.execute(sql,args)
			return True
		except Exception, e:
			return False

	def update(self,args,isbn):
		sql1 = "select id from publication where isbn = %s;"
		sql2 = "update publication set isbn = %s , title = %s , author = %s  \
			, pdate=%s , pcompany=%s , pagenum=%s , tags = %s \
			where id = %s;"
		try:
			with self._conn.cursor() as cur:
				cur.execute(sql1,(isbn,))
				idd = cur.fetchone()
				print idd
				print len(args)
				print cur.mogrify(sql2,args + (idd[u'id'],))
				cur.execute(sql2,args + (idd[u'id'],))
			return True
		except Exception ,e:
			return False


	def delete(self,isbn):
		sql = "delete from publication where isbn = %s"
		try:
			with self._conn.cursor() as cur:
				print cur.mogrify(sql,(isbn,))
				cur.execute(sql,(isbn,))
			return True
		except Exception,e:
			return False

	def searchText(self,pro,text,concret = False):
		""" pro can be title,isbn,author,pcompany,tags"""
		sql, param = self.textSearch(pro, text,concret)
		return self.search(sql,tuple(param))

	def searchCp(self,pro,text):
		dates = text.split("-")
		sql,param = self.cpSearch(pro, dates)
		return self.search(sql,tuple(param))

	def andSearch(self,paramlist,concret = False):
		sql = ""
		args = list()
		for i, text in enumerate(paramlist):
			if text == "":
				continue
			if i in (2,4):
				dates = text.split("-")
				print dates
				temp = self.cpSearch(self.prolist[i],dates)
			else:
				temp = self.textSearch(self.prolist[i],text,concret)
			if  temp[0].strip() == '()':
				continue
			print temp
			sql = " and %s " % temp[0] + sql
			args = temp[1] + args
		return self.search(sql[4:],args)

	def seniorSearch(self,param):
		pass
