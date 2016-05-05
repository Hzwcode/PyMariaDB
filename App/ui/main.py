#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from PyQt4 import QtGui, QtCore

import mytable,myAddBox
from database import pydb

app = QtGui.QApplication(sys.argv)

class main(QtGui.QMainWindow):
	def __init__(self, parent = None):
		QtGui.QMainWindow.__init__(self)

		self.db = pydb.mydb()

		#基本设置
		self.setWindowTitle(u'出版物管理系统')
		screen = QtGui.QDesktopWidget().screenGeometry()
		self.resize(1350, screen.height()/2);
		size = self.geometry()
		self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)
		self.statusBar().showMessage('statusbar')

		MainWidget = QtGui.QWidget(self)
		self.table = mytable.myTable(self)
		add_but = QtGui.QPushButton("add")
		del_but = QtGui.QPushButton("del")
		update_but = QtGui.QPushButton("update")
		sear_but = QtGui.QPushButton(u"搜索")
		senior_sear_but = QtGui.QPushButton(u"高级搜索")
		self.searchEdit = QtGui.QLineEdit()
		self.comboBox = QtGui.QComboBox()
		self.checkBox = QtGui.QRadioButton()

		self.comboBox.addItem(u"标题")
		self.comboBox.addItem(u"作者")
		self.comboBox.addItem(u"出版年")
		self.comboBox.addItem(u"出版社")
		self.comboBox.addItem(u"页数")
		self.comboBox.addItem(u"标签")
		self.comboBox.addItem(u"ISBN")

		"""
		update_but.clicked.connect(self.getLog)
		"""

		del_but.clicked.connect(self.delEvent)
		update_but.clicked.connect(self.updateEvent)
		add_but.clicked.connect(self.addEvent)
		sear_but.clicked.connect(self.searchEvent)
		senior_sear_but.clicked.connect(self.seniorSearchEvent)

		#layout
		hbox1 = QtGui.QHBoxLayout()
		hbox1.addWidget(self.checkBox)
		hbox1.addWidget(self.comboBox)
		hbox1.addWidget(self.searchEdit)
		hbox1.addWidget(sear_but)
		hbox1.addWidget(senior_sear_but)

		hbox2 = QtGui.QHBoxLayout()
		hbox2.addWidget(add_but)
		hbox2.addWidget(del_but)
		hbox2.addWidget(update_but)

		vbox = QtGui.QVBoxLayout()
		vbox.addStretch(1)
		vbox.addLayout(hbox1)
		vbox.addStretch(1)
		vbox.addWidget(self.table)
		vbox.setStretch(1, 2)
		vbox.setStretch(3, 30)
		vbox.addLayout(hbox2)

		self.setCentralWidget(MainWidget)
		MainWidget.setLayout(vbox)

	def searchEvent(self):
		index = self.comboBox.currentIndex()
		pro = self.db.prolist[index]
		text = unicode(self.searchEdit.text())
		concret = self.checkBox.isChecked()
		print index
		if index in (0,1,3,5,6):
			result = self.db.searchText(pro,text,concret)
			print result
			self.table.fullTable(result)
		else:
			result = self.db.searchCp(pro,text)
			self.table.fullTable(result)

	def seniorSearchEvent(self):
		box = myAddBox.myBox(parent = self,action = "search")
		box.searchSignal.connect(self.seniorSearchRecord)
		box.show()

	def addEvent(self):
		box = myAddBox.myBox(parent = self)
		box.addSignal.connect(self.addRecord)
		box.show()

	def updateEvent(self):
		param = self.table.getSelectedDate()
		if param == None:
			return
		box = myAddBox.myBox(parent = self,action = "update",param = param)
		box.updateSignal.connect(self.updateRecord)
		box.show()

	def seniorSearchRecord(self, texts):
		concret = self.checkBox.isChecked()
		result = self.db.andSearch(texts,concret)
		self.table.fullTable(result)

	def addRecord(self,param):
		param = (param[-1],) + param[:-1]
		if self.db.insert(param):
			self.db.commit()
			self.table.addRow(param,0)

	def updateRecord(self,param):
		if self.db.update((param[-1],) + param[:-1] ,self.table.getSelectedISBN()):
			self.db.commit()
			self.table.editRow(param)

	def delEvent(self):
		if self.table.selectedRow == -1:
			return
		ok = QtGui.QMessageBox.question(self, u"!!!!",u"确认删除",QtGui.QMessageBox.Yes,QtGui.QMessageBox.No)
		if ok == QtGui.QMessageBox.Yes:
			isbn = self.table.getSelectedISBN()
			if self.db.delete(isbn):
				self.db.commit()
				self.table.delSelectedRow()


	"""
	def addRule(self, param):
		self.table.addRow(param)
		mnf.addRule(param)

	def initRule(self):
		for param in mnf.rulelist:
			self.table.addRow(param)
		self.table.setCurRow(len(mnf.rulelist))

	def delEvent(self):
		row,ok = QtGui.QInputDialog.getInteger(self, u"删除",u"规则号",1,  1, 1 + len(mnf.rulelist))
		if ok:
			mnf.delRule(row - 1)
			self.table.removeRow(row - 1)
			self.table.setCurRow(len(mnf.rulelist))

	def getLog(self):
		mnf.getLog();

	def closeEvent(self,event):
		mnf.saveRule()
		mnf.mnf.close()
		mnf.rmmod()
		event.accept()
	"""


m = main()
m.show()
sys.exit(app.exec_())
