# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'electric_features_selection.ui'
#
# Created: Thu Set 1 12:38:15 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

import os
from PyQt5.QtWidgets import QDialog
from qgis.PyQt import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
os.path.dirname(__file__), 'electric_features_selection.ui'))

class Ui_Selection(QDialog, FORM_CLASS):

   def __init__(self, parent=None):
      """Constructor."""
      super(Ui_Selection, self).__init__(parent)
      self.setupUi(self)
