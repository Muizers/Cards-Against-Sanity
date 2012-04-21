#!/usr/bin/python2
# coding=utf-8
# NOTE: THIS PYTHON SOURCE FILE USES TABS DEAL WITH IT
#
# ⓒ 2012, Mark Harviston
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# Neither the name of the orgnanization nor the names of its
# contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
# USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

"""
The Main window GUI class, most gui operations here.

*** I REPEAT THIS PYTHON SOURCE FILE USES TABS, DEAL WITH IT ***
"""
import sys
import os.path

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView

#import code generated by gui designer ("View")
from main import Ui_MainWindow
from aboutDialog import Ui_aboutDialog

#import "Model" file
from cardsfile import CardsFile, BlackCard

app = QApplication(sys.argv)

def trace(fn):
	""" decorator Annotate function call with debugging info
	for now, just prints the name of the function"""

	def fn2(*args,**kwargs):
		print('tracing: ' + fn.__name__)
		return fn(*args,**kwargs)
	return fn2

class AboutDialog(QDialog, Ui_aboutDialog):
	def __init__(self, parent=None):
		super(type(self),self).__init__(parent)

		self.setupUi(self)

		self.okBtn.clicked.connect(self.onOK)

	def onOK(self):
		self.close()

class WhiteCardList(QAbstractListModel):
	def __init__(self, cardsfile):
		super(type(self),self).__init__()
		self.cardsfile = cardsfile

	def headerData(self,section, orientation, role=None):
		return ['Card Text']

	def rowCount(self, parent=None):
		return len(self.cardsfile.whitecards)

	def columnCount(self, parent=None):
		return 1

	def data(self, index, role=None):
		if index.isValid() and role == Qt.DisplayRole and index.column() == 0:
			return self.cardsfile.whitecards[index.row()]
		else:
			return None

class BlackCardList(QAbstractTableModel):
	def __init__(self, cardsfile):
		super(type(self),self).__init__()
		self.cardsfile = cardsfile

	def headerData(self, col, orientation, role=None):
		if role == Qt.DisplayRole:
			if col == 0:
				return 'Pick'
			elif col == 1:
				return 'Card Text'
			else:
				raise IndexError()
		else:
			return None

	def rowCount(self, parent=None):
		return len(self.cardsfile.blackcards)

	def columnCount(self, parent=None):
		return 2

	def data(self, index, role=None):
		if index.isValid() and role == Qt.DisplayRole:
			return self.cardsfile.blackcards[index.row()][index.column()]
		else:
			return None

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(type(self),self).__init__(parent)

		self.setupUi(self)

		#initialize model
		self.cardsfile = CardsFile()

		self.whiteModel = WhiteCardList(self.cardsfile)
		self.whiteList.setModel(self.whiteModel)
		
		self.blackModel = BlackCardList(self.cardsfile)
		self.blackList.setModel(self.blackModel)

		#connect signals
		self.addWhiteBtn.clicked.connect(self.addWhiteCard)
		self.removeWhiteBtn.clicked.connect(self.remWhiteCard)
		self.addBlackBtn.clicked.connect(self.addBlackCard)
		self.removeBlackBtn.clicked.connect(self.remBlackCard)

		self.actionNew.triggered.connect(self.menuNew)
		self.actionOpen.triggered.connect(self.menuOpen)
		self.actionSave.triggered.connect(self.menuSave)
		self.actionSaveAs.triggered.connect(self.menuSaveAs)
		self.actionPrintPreview.triggered.connect(self.menuPrintPreview)
		self.actionExportPDF.triggered.connect(self.menuExportPDF)
		self.actionExportFO.triggered.connect(self.menuExportFO)

		self.actionAbout.triggered.connect(self.menuAbout)

	def menuAbout(self):
		aboutDlg = AboutDialog(self)
		aboutDlg.show()
		aboutDlg.raise_()

	def addWhiteCard(self):
		pass #TODO

	def remWhiteCard(self):
		pass #TODO

	def addBlackCard(self):
		pass #TODO

	def remBlackCard(self):
		pass #TODO

	def menuNew(self):
		pass #TODO

	def menuOpen(self):
		fileName, _ = QFileDialog.getOpenFileName(self, 'Open Cards Against Humanity File', None, 'Cards Against Humanity File (*.cah, *.xml)')
		print('filename: %s' % fileName)

		self.cardsfile.importXML(fileName)
		self.whiteModel.dataChanged.emit(None,None)

	def menuSave(self):
		if self.cardsfile.filename is not None:
			self.cardsfile.save()
		else:
			self.menuSaveAs()

	def menuSaveAs(self):
		self.cardsfile.filename, _ = QFileDialog.getSaveFileName(self, 'Save Cards Against Humanity File', \
			self.cardsfile.filename, 'Cards Against Humanity File (*.cah, *.xml)')
		self.cardsfile.save()

	def menuExportPDF(self):
		if self.cardsfile.filename is not None:
			dirname = os.path.dirname(self.cardsfile.filename)
		else:
			dirname = None

		fileName, _ = QFileDialog.getSaveFileName(self, 'Export PDF File', dirname, 'Portable Document Format (*.pdf)')
		self.cardsfile.exportToPDF(fileName)

	def menuExportFO(self):
		if self.cardsfile.filename is not None:
			dirname = os.path.dirname(self.cardsfile.filename)
		else:
			dirname = None

		fileName, _ = QFileDialog.getSaveFileName(self, 'Export XSL Formatting Objects File', dirname, 'XSL Formatting Objects File (*.fo, *.xml)')
		self.cardsfile.exportToFO(fileName)

	def menuPrintPreview(self):
		self.cardsfile.printPreview()

if __name__ == '__main__':
	win = MainWindow()
	win.show()
	win.raise_()

	sys.exit(app.exec_())

	app.exec_()
	sys.exit()
