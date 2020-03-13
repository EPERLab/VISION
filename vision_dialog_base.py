# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vision_dialog_base.ui'
#
# Created: Wed Feb 22 14:14:30 2017
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from builtins import object
from qgis.PyQt import QtCore, QtGui
from PyQt5 import QtGui #Paquetes requeridos para crear ventanas de diálogo e interfaz gráfica.
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QDialog, QStyleFactory, QDialogButtonBox
import traceback

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_VISIONDialogBase(object):
    def setupUi(self, VISIONDialogBase):
        VISIONDialogBase.setObjectName(_fromUtf8("VISIONDialogBase"))
        VISIONDialogBase.resize(400, 300)
        self.button_box = QDialogButtonBox(VISIONDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))

        self.retranslateUi(VISIONDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), VISIONDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), VISIONDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(VISIONDialogBase)

    def retranslateUi(self, VISIONDialogBase):
        VISIONDialogBase.setWindowTitle(_translate("VISIONDialogBase", "VISION", None))

