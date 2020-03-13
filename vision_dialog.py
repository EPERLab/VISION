# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VISIONDialog
                                 A QGIS plugin
 This plugin graduate points and lines layers with a defined ramp color, generate heatmaps and recreate the grid behaviour through animations 
                             -------------------
        begin                : 2017-02-22
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Marco Jara Jiménez
        email                : marco.jara@ucr.ac.cr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.PyQt import QtGui, uic
from PyQt5.QtWidgets import QDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'vision_dialog_base.ui'))


class VISIONDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(VISIONDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
