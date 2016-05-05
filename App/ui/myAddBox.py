#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class myBox(QtGui.QDialog):
	actions = {
		"insert": u"添加记录",
		"update": u"修改记录",
		"search": u"搜索记录"
	}
	addSignal = QtCore.pyqtSignal(tuple)
	updateSignal = QtCore.pyqtSignal(tuple)
	searchSignal = QtCore.pyqtSignal(tuple)
	def __init__(self, action = "insert", param = ("",)*7, parent = None):
		QtGui.QDialog.__init__(self,parent)

		self.act = action
		self.setWindowTitle(self.actions[action])
		self.resize(350,400)
		self.grid = QtGui.QGridLayout(self)

		title_lab = QtGui.QLabel(u"标题",self)
		author_lab = QtGui.QLabel(u"作者",self)
		tm_lab = QtGui.QLabel(u"出版年", self)
		press_lab = QtGui.QLabel(u"出版社", self)
		pages_lab = QtGui.QLabel(u"页数", self)
		tags_lab = QtGui.QLabel(u"标签",self)
		isbn_lab = QtGui.QLabel(u"ISBN",self)

		if self.act == "search":
			tm_validator = QtGui.QRegExpValidator(QtCore.QRegExp (u"[0-9-]{,4}"))
		else:
			tm_validator = QtGui.QIntValidator(0, 9999,self)
		pages_validator = QtGui.QIntValidator(0,10000,self)
		ISBN_validator = QtGui.QRegExpValidator(QtCore.QRegExp (u"[0-9]{10}([0-9]{3})?"))

		self.title_box = QtGui.QLineEdit(param[0])
		self.author_box = QtGui.QLineEdit(param[1])
		self.tm_box = QtGui.QLineEdit(param[2])
		self.press_box = QtGui.QLineEdit(param[3])
		self.pages_box = QtGui.QLineEdit(param[4])
		self.tags_box = QtGui.QLineEdit(param[5])
		self.isbn_box = QtGui.QLineEdit(param[6])

		self.boxs = (self.title_box,self.author_box,self.tm_box,self.press_box,self.pages_box,self.tags_box,self.isbn_box)

		self.tm_box.setValidator(tm_validator)
		self.isbn_box.setValidator(ISBN_validator)
		self.pages_box.setValidator(pages_validator)

		yes = QtGui.QPushButton(u"确定")
		no = QtGui.QPushButton(u"取消")

		self.grid.addWidget(title_lab, 0, 0)
		self.grid.addWidget(author_lab, 1, 0)
		self.grid.addWidget(press_lab, 3, 0)
		self.grid.addWidget(tm_lab, 2, 0)
		self.grid.addWidget(pages_lab, 4, 0)
		self.grid.addWidget(tags_lab, 5, 0)
		self.grid.addWidget(isbn_lab, 6, 0)

		self.grid.addWidget(self.title_box, 0, 1, 1, 4)
		self.grid.addWidget(self.author_box, 1, 1, 1, 4)
		self.grid.addWidget(self.press_box, 3, 1, 1, 4)
		self.grid.addWidget(self.tm_box, 2, 1, 1, 4)
		self.grid.addWidget(self.pages_box, 4, 1, 1, 4)
		self.grid.addWidget(self.tags_box, 5, 1, 1, 4)
		self.grid.addWidget(self.isbn_box, 6, 1, 1, 4)

		self.grid.addWidget(yes,7,0,1,2)
		self.grid.addWidget(no,7,4,1,2)

		yes.clicked.connect(self.yesEvent)
		no.clicked.connect(self.noEvent)

	def yesEvent(self):
		#搜索事件
		if self.act == "search":
			param = self.appendBox()
			print param
			self.searchSignal.emit(tuple(param))
			self.close()
			return

		param = self.checkBox()
		if param == False:
			return;
		param = tuple(param)
		if self.act == "insert":
			self.addSignal.emit(param)
		elif self.act == "update":
			self.updateSignal.emit(param)
		self.close()

	def appendBox(self):
		param = list()
		for i,box in enumerate(self.boxs):
			text = box.text().trimmed()
			param.append(unicode(text))
		return param

	def checkBox(self):
		param = list()
		for i,box in enumerate(self.boxs):
			text = box.text().trimmed()
			if i == 5:
				param.append(unicode(text))
				continue
			if text == "":
				return False
			param.append(unicode(text))
		else:
			return param

	def noEvent(self):
		self.close()
