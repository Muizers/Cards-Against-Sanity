from PySide.QtCore import *
from PySide.QtGui import *

class ComboBoxDelegate(QStyledItemDelegate):
	"""
	copied extensively from here: http://stackoverflow.com/questions/10037529/custom-delegate-in-pyside
	"""

	def __init__(self, model, parent=None):
		super(type(self), self).__init__(parent)
		self.parent= parent
		self.model= model

	def createEditor(self, parent, option, index):

		if not index.isValid():
			return False

		self.currentIndex=index

		self.comboBox = QComboBox(parent)
		self.comboBox.setModel(self.model)
		value = index.data(Qt.DisplayRole)
		self.comboBox.setCurrentIndex(value)

		return self.comboBox

	def setEditorData(self, editor, index):
		value = index.data(Qt.DisplayRole)
		editor.setCurrentIndex(value)

	def setModelData(self, editor, model, index):

		if not index.isValid():
			return False

		index.model().setData(index, editor.currentIndex(), Qt.EditRole)
