#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class myTable(QtGui.QTableWidget):
	"""docstring for myTable"""
	def __init__(self, parent = None):
		QtGui.QTableWidget.__init__(self, parent)
		#self.resize(100,200)
		self.setMinimumWidth(600)
		#列表格式初始化
		self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.setColumnCount(7)
		self.setRowCount(15)
		self.curRow = 0
		self.selectedRow = -1

		header = [u"标题", u"作者",u"出版年",u"出版社",u"页数",u"标签",u"ISBN"]
		self.setHorizontalHeaderLabels(header)

		self.setColumnWidth(0, 260)
		self.setColumnWidth(1, 200)
		self.setColumnWidth(2, 100)
		self.setColumnWidth(3, 180)
		self.setColumnWidth(4, 80)
		self.setColumnWidth(5, 320)
		self.setColumnWidth(6, 150)

		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		self.cellClicked.connect(self.rowClicked)
		#self.connect(self,QtCore.SIGNAL(cellDoubleClicked),QtCore.SLOT(self.rowClick))

	def addRow(self,param, row = None):
		prolist = (u"title",u"author",u"pdate",u"pcompany",u"pagenum",u"tags",u"isbn")
		if len(param) != 7:
			print "not enough argument in addRow"
			return
		print param
		curRow = self.curRow
		if row != None:
			self.insertRow(0)
			curRow = 0
		for i, par in enumerate(param):
			if isinstance(param,tuple):
				k = (i + 1) % 7
				text = param[k]
			elif isinstance(param,dict):
				text = param[prolist[i]]
			if isinstance(text,str):
				text = text.decode('utf8')
			elif isinstance(text,int):
				text = unicode(text)
			item = QtGui.QTableWidgetItem(text)
			item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
			self.setItem(curRow, i,item)
		self.curRow += 1

	def editRow(self,param,row = None):
		if len(param) != 7:
			print "not enough argument in addRow"
			return
		if row == None:
			row = self.selectedRow
		print param
		for i, par in enumerate(param):
			k = i % 7
			text = param[k]
			if isinstance(text,str):
				text = text.decode('utf8')
			elif isinstance(text,int):
				text = unicode(text)
			item = self.item(row,k)
			item.setText(text)

	def delRow(self,row):
		self.removeRow(row)

	def delSelectedRow(self):
		self.delRow(self.selectedRow)

	def fullTable(self, paramlist):
		self.clearContents()
		self.curRow = 0
		print len(paramlist)
		if len(paramlist) > 15:
			self.setRowCount(len(paramlist))
		else:
			self.setRowCount(15)
		for param in paramlist:
			#param = param[:-1]
			self.addRow(param)

	def setCurRow(self, row):
		self.curRow = row

	def rowClicked(self,row,col):
		print row
		if self.item(row,0) == None:
			self.selectedRow = -1
		else:
			self.selectedRow = row

	def getSelectedISBN(self):
		if self.selectedRow == -1:
			return None
		return unicode(self.item(self.selectedRow, 6).text().trimmed())

	def getSelectedDate(self):
		if self.selectedRow == -1:
			return None
		param = list()
		for i in xrange(7):
			item = self.item(self.selectedRow,i)
			param.append(unicode(item.text().trimmed()))
		return param
