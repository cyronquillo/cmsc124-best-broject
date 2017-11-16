# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from interpreter import *

class Ui_Dialog(QWidget):
	def selectFile(self):
		try:
			f = open(QtWidgets.QFileDialog.getOpenFileName()[0], "r")
			self.textEdit_2.setText(f.read())
			f.close()
		except:
			pass

	def saveFile(self):
		try:
			f = open(QtWidgets.QFileDialog.getOpenFileName()[0], "w+")
			f.write(self.textEdit_2.toPlainText())
			f.close()
		except:
			pass

	def executeCode(self):
		self.interpreter.sym_table.clear()
		self.tableWidget_2.setRowCount(0)
		self.interpreter.inp = self.textEdit_2.toPlainText()
		self.interpreter.make_lex_table()
		self.interpreter.run_program()
		self.tableWidget.setRowCount(0)
		self.tableWidget.setRowCount(len(self.interpreter.lex_table))

		for i, row in enumerate(self.interpreter.lex_table):
			token = QtWidgets.QTableWidgetItem(row[0])
			type = QtWidgets.QTableWidgetItem(row[1])
			self.tableWidget.setItem(i, 0, token)
			self.tableWidget.setItem(i, 1, type)

	def updateSymbolTable(self):
		self.tableWidget_2.setRowCount(0)
		self.tableWidget_2.setRowCount(len(self.interpreter.sym_table))

		i = 0
		for varname, value in self.interpreter.sym_table.items():
			token = QtWidgets.QTableWidgetItem(varname)
			type = QtWidgets.QTableWidgetItem(str(value[0]))
			self.tableWidget_2.setItem(i, 0, token)
			self.tableWidget_2.setItem(i, 1, type)
			i += 1


	def __init__(self, app):
		super(Ui_Dialog, self).__init__()
		self.app = app
		self.interpreter = Interpreter("", self)


	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.setEnabled(True)
		Dialog.resize(905, 549)
		Dialog.setWindowTitle("ANG GANDA NI MA\'AM KAT LOLTERPRETER")
		Dialog.setAutoFillBackground(False)
		Dialog.setModal(False)
		self.tableWidget = QtWidgets.QTableWidget(Dialog)
		self.tableWidget.setGeometry(QtCore.QRect(300, 90, 301, 261))
		self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
		self.tableWidget.setRowCount(2)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setObjectName("tableWidget")
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setFamily("Monospace")
		item.setFont(font)
		self.tableWidget.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setFamily("Monospace")
		item.setFont(font)
		self.tableWidget.setHorizontalHeaderItem(1, item)
		self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
		self.tableWidget.horizontalHeader().setStretchLastSection(True)
		self.textEdit_2 = QtWidgets.QTextEdit(Dialog)
		self.textEdit_2.setGeometry(QtCore.QRect(10, 90, 281, 261))
		self.textEdit_2.setObjectName("textEdit_2")
		font = QtGui.QFont()
		font.setFamily("Monospace")
		font.setPointSize(8);
		self.textEdit_2.setFont(font)
		self.textEdit_3 = QtWidgets.QTextEdit(Dialog)
		self.textEdit_3.setGeometry(QtCore.QRect(10, 390, 881, 151))
		font = QtGui.QFont()
		font.setFamily("Monospace")
		font.setPointSize(8);
		self.textEdit_3.setFont(font)
		self.textEdit_3.setAutoFillBackground(False)
		self.textEdit_3.setReadOnly(True)
		self.textEdit_3.setObjectName("textEdit_3")

		font = QtGui.QFont()
		font.setFamily("Monospace")
		self.pushButton = QtWidgets.QPushButton(Dialog)
		self.pushButton.setGeometry(QtCore.QRect(10, 20, 111, 34))
		font = QtGui.QFont()
		font.setFamily("Monospace")
		self.pushButton.setFont(font)
		self.pushButton.setObjectName("pushButton")
		self.pushButton_2 = QtWidgets.QPushButton(Dialog)
		self.pushButton_2.setGeometry(QtCore.QRect(130, 20, 101, 34))

		self.pushButton.setAutoDefault(False)
		self.pushButton_2.setAutoDefault(False)
		self.pushButton.clicked.connect(self.executeCode)
		self.pushButton_2.clicked.connect(self.selectFile)

		font = QtGui.QFont()
		font.setFamily("Monospace")
		self.pushButton_2.setFont(font)
		self.pushButton_2.setObjectName("pushButton_2")

		self.pushButton_3 = QtWidgets.QPushButton(Dialog)
		self.pushButton_3.setGeometry(QtCore.QRect(240, 20, 111, 34))
		font = QtGui.QFont()
		font.setFamily("Monospace")
		self.pushButton_3.setFont(font)
		self.pushButton_3.setObjectName("pushButton")
		self.pushButton_3.setAutoDefault(False)
		self.pushButton_3.clicked.connect(self.saveFile)

		self.tableWidget_2 = QtWidgets.QTableWidget(Dialog)
		self.tableWidget_2.setGeometry(QtCore.QRect(610, 90, 281, 261))
		self.tableWidget_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		self.tableWidget_2.setGridStyle(QtCore.Qt.SolidLine)
		self.tableWidget_2.setRowCount(0)
		self.tableWidget_2.setColumnCount(2)
		self.tableWidget_2.setObjectName("tableWidget_2")
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setFamily("Monospace")
		item.setFont(font)
		self.tableWidget_2.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		font = QtGui.QFont()
		font.setFamily("Monospace")
		item.setFont(font)
		self.tableWidget_2.setHorizontalHeaderItem(1, item)
		self.tableWidget_2.horizontalHeader().setDefaultSectionSize(100)
		self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
		self.label_3 = QtWidgets.QLabel(Dialog)
		self.label_3.setGeometry(QtCore.QRect(20, 60, 211, 18))
		font = QtGui.QFont()
		font.setFamily("Monospace")
		self.label_3.setFont(font)
		self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
		self.label_3.setObjectName("label_3")
		self.label_4 = QtWidgets.QLabel(Dialog)
		self.label_4.setGeometry(QtCore.QRect(20, 360, 58, 18))
		font = QtGui.QFont()
		font.setFamily("Monospace")
		self.label_4.setFont(font)
		self.label_4.setObjectName("label_4")
		self.label_5 = QtWidgets.QLabel(Dialog)
		self.label_5.setGeometry(QtCore.QRect(300, 60, 211, 18))
		font = QtGui.QFont()
		font.setFamily("Monospace")
		self.label_5.setFont(font)
		self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
		self.label_5.setObjectName("label_5")
		self.label_6 = QtWidgets.QLabel(Dialog)
		self.label_6.setGeometry(QtCore.QRect(610, 60, 211, 18))
		font = QtGui.QFont()
		font.setFamily("Monospace")
		self.label_6.setFont(font)
		self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
		self.label_6.setObjectName("label_6")
		self.tableWidget.raise_()
		self.textEdit_2.raise_()
		self.textEdit_3.raise_()
		self.pushButton.raise_()
		self.pushButton_2.raise_()
		self.tableWidget_2.raise_()
		self.label_3.raise_()
		self.label_4.raise_()
		self.label_5.raise_()
		self.label_6.raise_()

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		item = self.tableWidget.horizontalHeaderItem(0)
		item.setText(_translate("Dialog", "Lexeme"))
		item = self.tableWidget.horizontalHeaderItem(1)
		item.setText(_translate("Dialog", "Classification"))
		self.pushButton.setText(_translate("Dialog", "Execute Code"))
		self.pushButton_2.setText(_translate("Dialog", "Open File"))
		self.pushButton_3.setText(_translate("Dialog", "Save File"))
		item = self.tableWidget_2.horizontalHeaderItem(0)
		item.setText(_translate("Dialog", "Identifier"))
		item = self.tableWidget_2.horizontalHeaderItem(1)
		item.setText(_translate("Dialog", "Value"))
		self.label_3.setText(_translate("Dialog", "Code"))
		self.label_4.setText(_translate("Dialog", "Console"))
		self.label_5.setText(_translate("Dialog", "Lexeme Table"))
		self.label_6.setText(_translate("Dialog", "Symbol Table"))

	def showDialog(self):
		text,ok = QInputDialog.getText(self, 'Input', 'Enter Input')
		if ok:
			return str(text)
		else:
			return ""

	def printConsole(self, out):
		self.textEdit_3.insertPlainText(out)
