# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VISION
                                 A QGIS plugin
 This plugin graduate points and lines layers with a defined ramp color, generate heatmaps and recreate the grid behaviour through animations 
                             -------------------
        begin                : 2017-02-22
        copyright            : (C) 2017 by Marco Jara Jiménez
        email                : marco.jara@ucr.ac.cr
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load VISION class from file VISION.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .vision import VISION
    return VISION(iface)
