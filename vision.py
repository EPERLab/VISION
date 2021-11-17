"""
/***************************************************************************
 VISION
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
from __future__ import print_function
from __future__ import absolute_import
# Initialize Qt resources from file resources.py
from builtins import map
from builtins import str
from builtins import range
from builtins import object
from . import resources
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
from qgis.analysis import *
import processing
import time
import qgis
import sys

from PyQt5 import QtGui #Paquetes requeridos para crear ventanas de diálogo e interfaz gráfica.
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox, QDialog, QStyleFactory, QAction
import traceback

#from datetime import datetime, date, time, timedelta
#import calendar
# Import the code for the dialog
from .vision_dialog import VISIONDialog
import os.path
from .electric_features_selection import Ui_Selection


class VISION(object):

    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'VISION_{}.qm'.format(locale))
        
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

            
        # if locale != (u'es'): # esp
            # locale = (u'en')  #eng
    
                
        # Create the dialog (after translation) and keep reference
        self.dlg = VISIONDialog()
        self.selection = Ui_Selection()
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&VISION')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'VISION')
        self.toolbar.setObjectName(u'VISION')
        self.dlg.CategButton.clicked.connect(self.VoltCateg)
        self.dlg.HeatButton.clicked.connect(self.Hotest)
        self.dlg.GraduateLButton.clicked.connect(self.linesGradua)
        self.dlg.CategTxButton.clicked.connect(self.categTx)
        self.dlg.button_box.helpRequested.connect(self.show_help)
        
        self.dlg.comboBox_cap_categ_tension.currentIndexChanged.connect(self.changeCategVoltage_Categ)
        self.dlg.comboBox_cap_heatmap.currentIndexChanged.connect(self.changeHeatMap_Categ)
        self.dlg.comboBox_cap_catTraf.currentIndexChanged.connect(self.changeFluxTrafo_Categ)
        self.dlg.comboBox_cap_gradLine.currentIndexChanged.connect(self.changeFluxLines_Grad)
        

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('VISION', message)
        
        

    #Función que se encarga de imprimir los errores que han ocurrido
    def print_error(self):
        exc_info = sys.exc_info()
        print("\nError: ", exc_info )
        print("*************************  Información detallada del error ********************")
        for tb in traceback.format_tb(sys.exc_info()[2]):
            print(tb)
        return
        
    def IdentifyAtribut(self): # Método para llamar el main del attributes selection
        #This block obtains the attributes in the active layer and append them the in the combo boxes
        #selectedLayer = iface.activeLayer()
        
        nameLayer = self.dlg.comboBox_cap_atrib.currentText()  #
        
        if nameLayer == "" or nameLayer == None:
            aviso = "Seleccione una capa válida"
            QMessageBox.warning(None, QCoreApplication.translate('dialog', "Error"), aviso)
            return
        selectedLayer = QgsProject.instance().mapLayersByName(nameLayer)[0] #Se selecciona la capa de la base de datos "layers" según el índice de layer_list
        """
        datosLayer = selectedLayer.getFeatures()
        prop =selectedLayer.dataProvider()
        attr_list = []
        fields= prop.fields()
        for field in fields:
            attr_list.append(field.name())
        global Att1
        global Att2
        global Att3
        
        #self.selection.combo_Atrib1.clear()		
        self.selection.combo_Atrib1.addItems(attr_list)
        Att1 = self.dlg.combo_Atrib1.currentText()
        #self.selection.combo_Atrib2.clear()		
        self.selection.combo_Atrib2.addItems(attr_list)
        Att2 = self.selection.combo_Atrib2.currentText()
        #self.selection.combo_Atrib3.clear()		
        self.selection.combo_Atrib3.addItems(attr_list)
                
        
        self.selection.exec_()
        """
        
        global Att1
        global Att2
        global Att3
        
        Att1 = self.dlg.combo_Atrib1.currentText()
        Att2 = self.selection.combo_Atrib2.currentText()
        Att3 = self.selection.combo_Atrib3.currentText()
        
        iface.messageBar().pushMessage("Finalizado", "Identificación de atributos finalizada", level=Qgis.Success, duration=3)
             
             
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        #self.dlg = VISIONDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/VISION/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'VISION'),
            callback=self.run,
            parent=self.iface.mainWindow())
    
    def getAttributeIndex(self, aLayer, attrName): # Crea el atributo y obtiene el ID
        #Find the attribute index, adding a new Int column, if necessary
        # TODO: If attrName is longer than 10, something fails later.  Move validation to a signal that checks storageType in the UI.
        if len(attrName) > 10 and aLayer.storageType() == 'ESRI Shapefile':
            self.iface.messageBar().pushCritical("Error", "For ESRI Shapefiles, the maximum length of any attribute name is 10. Please choose a shorter attribute name.")
            return -3
        AttrIdx = aLayer.dataProvider().fieldNameIndex(attrName)
        if AttrIdx == -1: # attribute doesn't exist, so create it
            caps = aLayer.dataProvider().capabilities()
            if caps & QgsVectorDataProvider.AddAttributes:
                res = aLayer.dataProvider().addAttributes([QgsField(attrName, QVariant.String)])
                AttrIdx = aLayer.dataProvider().fieldNameIndex(attrName)
                aLayer.updateFields()
                if AttrIdx == -1:
                    self.iface.messageBar().pushCritical("Error", "Failed to create attribute!")
                    return -1
            else:
                self.iface.messageBar().pushCritical("Error", "Failed to add attribute!")
                return -1
        else:
            pass
        return AttrIdx
        
    def show_help(self):
        """Display application help to the user."""
   
        help_file = 'file:///%s/help/Manual_VISION.pdf' % self.plugin_dir
        # For testing path:
        #QMessageBox.information(None, 'Help File', help_file)
        # noinspection PyCallByClass,PyTypeChecker
        QDesktopServices.openUrl(QUrl(help_file))
        
    def matchFeatures(self): # Método para realizar el match de features entre la capa de lineCurrents y las capas de líneas
        layers = list( QgsProject.instance().mapLayers().values() )
        layer_list = []
        layer_list.append("")
        for layer in layers:
            layer_list.append(layer.name())
        layers.insert(0,"")
        
        LineCurrents = QgsProject.instance().mapLayersByName('lineCurrents')
        
        if LineCurrents == []:
            aviso = "Se debe proporcionar la capa lineCurrents en el proyecto GIS. Favor agregarla y volver a intentar"
            QMessageBox.warning(None, "Error lineCurrents", aviso)
            return
        LineCurrents = LineCurrents[0]
        flowLayer = LineCurrents.getFeatures()
        z = LineCurrents.dataProvider().attributeIndexes()
        sn = LineCurrents.dataProvider().fieldNameIndex('PFsnap')
        zv = int(len(z)) -1
        
        Dicti = {}
        for m in flowLayer:
            PFlist = []
            Dicti[str(m['DSSName'])]=[]
            if sn != -1:
                
                for k in range(zv-1): # Es el total de atributos de flujo - el Snapshot
                    PFlist.append(m['PF'+str(k)])
                #PFlist.append(m['PFsnap'])
                Dicti[str(m['DSSName'])].append(PFlist)
                Dicti[str(m['DSSName'])].append(m['PFsnap'])
            
            elif sn == -1:
                for k in range(zv): # El valor de zv sera el tope ya que no hay snapshot
                    PFlist.append(m['PF'+str(k)])
            
                Dicti[str(m['DSSName'])].append(PFlist)
            
        
        Lineslayers = []
        
        if self.dlg.comboBox_Lins.currentIndex() != 0:
            Lineslayers.append(layers[self.dlg.comboBox_Lins.currentIndex()])
        if self.dlg.comboBox_Lins2.currentIndex() != 0:
            Lineslayers.append(layers[self.dlg.comboBox_Lins2.currentIndex()])
        if self.dlg.comboBox_Lins3.currentIndex() != 0:
            Lineslayers.append(layers[self.dlg.comboBox_Lins3.currentIndex()])
        if self.dlg.comboBox_Lins4.currentIndex() != 0:
            Lineslayers.append(layers[self.dlg.comboBox_Lins4.currentIndex()])
        
        for lay in Lineslayers:
            caps = lay.dataProvider().capabilities() #es para averiguar las capacidades de la capa 
            lay.startEditing()   
            if sn != -1:
                
                for k in range(zv-1):  #el range debería ser la longitud de atributos que posee la capa lineCurrents sin contar Snap
                    Idx = self.getAttributeIndex(lay, 'PF'+str(k))
                    if caps & QgsVectorDataProvider.ChangeAttributeValues:
                        
                        lineFeat = lay.getFeatures()
                        for line in lineFeat:
                            a=Dicti[line['DSSName']][0][k]
                            lay.changeAttributeValue(line.id(), Idx, a) #id, Index, Value str(Dicti[line['DSSName']][0][k])
                Idx = self.getAttributeIndex(lay, 'PFsnap')
                
                if caps & QgsVectorDataProvider.ChangeAttributeValues:
                        
                    lineFeat = lay.getFeatures()
                    for line in lineFeat:
                        try:
                            a=Dicti[line['DSSName']][1] 
                            lay.changeAttributeValue(line.id(), Idx, a) #id, Index, Value str(Dicti[line['DSSName']][0][k])
                        except KeyError: self.print_error()
                         
                    #lay.commitChanges()
                    #lay.updateFields()
                lay.commitChanges()
                lay.updateFields()
            
            
            elif sn == -1:
                for k in range(zv):  #el range debería ser la longitud de atributos que posee la capa lineCurrents
                        #item.append(str(Dicti[item['DSSName'][k]))#Att1 son los pf's
                        
                    Idx = self.getAttributeIndex(lay, 'PF'+str(k))
                    if caps & QgsVectorDataProvider.ChangeAttributeValues:
                        
                        lineFeat = lay.getFeatures()
                        for line in lineFeat:
                            a=Dicti[line['DSSName']][0][k]
                           
                            lay.changeAttributeValue(line.id(), Idx, a) #id, Index, Value str(Dicti[line['DSSLine']][0][k])
                lay.commitChanges()
                lay.updateFields()
        
        iface.messageBar().pushInfo("INFO", QCoreApplication.translate('menu', 'Proceso terminado exitosamente'))  
        return
    
    
    def matchFeaturesTx(self): # Método para realizar el match de features entre la capa de lineCurrents y las capas de líneas
        layers = list( QgsProject.instance().mapLayers().values() )
        layer_list = []
        layer_list.append("")
        for layer in layers:
            layer_list.append(layer.name())
        txCapacities = QgsProject.instance().mapLayersByName('txCapacities')
        
        if txCapacities == []:
            aviso = "Se debe proporcionar la capa txCapacities en el proyecto GIS. Favor agregarla y volver a intentar"
            QMessageBox.warning(None, "Error txCapacities", aviso)
            return
        
        txCapacities = txCapacities[0]
        flowLayer = txCapacities.getFeatures()
        z = txCapacities.dataProvider().attributeIndexes()
        sn = txCapacities.dataProvider().fieldNameIndex('PFsnap')
        zv = int(len(z)) -1
        print(('capas PFs total zv',zv))
        print(('atri snap sn',sn))
        
        Dicti = {}
        for m in flowLayer:
            PFlist = []
            Dicti[str(m['DSSName'])]=[]
            if sn != -1:
                
                for k in range(zv-1): # Es el total de atributos de flujo - el Snapshot
                    PFlist.append(m['PF'+str(k)])
                #PFlist.append(m['PFsnap'])
                Dicti[str(m['DSSName'])].append(PFlist)
                Dicti[str(m['DSSName'])].append(m['PFsnap'])
            
            elif sn == -1:
                for k in range(zv): # El valor de zv sera el tope ya que no hay snapshot
                    PFlist.append(m['PF'+str(k)])
            
                Dicti[str(m['DSSName'])].append(PFlist)
                
        Lineslayers = []
          # Recibe la capa de subestación seleccionada en la lista desplegable
        
        if self.dlg.comboBox_Tx1.currentIndex() != 0:
            Lineslayers.append(layers[self.dlg.comboBox_Tx1.currentIndex()])
        if self.dlg.comboBox_Tx2.currentIndex() != 0:
            Lineslayers.append(layers[self.dlg.comboBox_Tx2.currentIndex()])
        
        for lay in Lineslayers:
            caps = lay.dataProvider().capabilities() #es para averiguar las capacidades de la capa 
            lay.startEditing()   
            if sn != -1:
                
                for k in range(zv-1):  #el range debería ser la longitud de atributos que posee la capa lineCurrents sin contar Snap
                    Idx = self.getAttributeIndex(lay, 'PF'+str(k))
                    if caps & QgsVectorDataProvider.ChangeAttributeValues:
                        
                        lineFeat = lay.getFeatures()
                        for line in lineFeat:
                            a=Dicti[line['DSSName']][0][k]
                           
                            lay.changeAttributeValue(line.id(), Idx, a) #id, Index, Value str(Dicti[line['DSSLine']][0][k])
                            
                Idx = self.getAttributeIndex(lay, 'PFsnap')
                if caps & QgsVectorDataProvider.ChangeAttributeValues:
                        
                    lineFeat = lay.getFeatures()
                    for line in lineFeat:
                        try:
                            a=Dicti[line['DSSName']][1] 
                            lay.changeAttributeValue(line.id(), Idx, a) #id, Index, Value str(Dicti[line['DSSName']][0][k])
                        except KeyError: self.print_error()
            
                            
                
                lay.commitChanges()
                lay.updateFields()
            
            
            elif sn == -1:
                for k in range(zv):  #el range debería ser la longitud de atributos que posee la capa lineCurrents
                        #item.append(str(Dicti[item['DSSName'][k]))#Att1 son los pf's
                        
                    Idx = self.getAttributeIndex(lay, 'PF'+str(k))
                    if caps & QgsVectorDataProvider.ChangeAttributeValues:
                        
                        lineFeat = lay.getFeatures()
                        for line in lineFeat:
                            a=Dicti[line['DSSName']][0][k]
                           
                            lay.changeAttributeValue(line.id(), Idx, a) #id, Index, Value str(Dicti[line['DSSLine']][0][k])
                lay.commitChanges()
                lay.updateFields()
        
        iface.messageBar().pushInfo("INFO", QCoreApplication.translate('menu', 'Proceso terminado exitosamente'))  
    
    
    #Función llamada cuando se da un cambio en comboBox_cap_categ_tension. Se encarga a su vez de cambiar el dato en ColorRampAttri
    def changeCategVoltage_Categ(self):
        combo_box_attri = self.dlg.ColorRampAttri
        combo_box_attri.clear()
        nameLayer = self.dlg.comboBox_cap_categ_tension.currentText()  # Recibe la capa de subestación seleccionada en la lista desplegable
        if nameLayer == "" or nameLayer == None:
            return
        selectedLayer = QgsProject.instance().mapLayersByName(nameLayer)[0] #Se selecciona la capa de la base de datos "layers" según el índice
        self.charge_attributes(selectedLayer, combo_box_attri)
        return
        
    #Función llamada cuando se da un cambio en comboBox_cap_heatmap. Se encarga a su vez de cambiar el dato en HeatmapAttri
    def changeHeatMap_Categ(self):
        combo_box_attri = self.dlg.HeatmapAttri
        combo_box_attri.clear()
        nameLayer = self.dlg.comboBox_cap_heatmap.currentText()  # Recibe la capa de subestación seleccionada en la lista desplegable
        if nameLayer == "" or nameLayer == None:
            return
        selectedLayer = QgsProject.instance().mapLayersByName(nameLayer)[0] #Se selecciona la capa de la base de datos "layers" según el índice
        self.charge_attributes(selectedLayer, combo_box_attri)
        return
        
    #Función llamada cuando se da un cambio en comboBox_cap_catTraf. Se encarga a su vez de cambiar el dato en TxLoad
    def changeFluxTrafo_Categ(self):
        combo_box_attri = self.dlg.TxLoad
        combo_box_attri.clear()
        nameLayer = self.dlg.comboBox_cap_catTraf.currentText()  # Recibe la capa de subestación seleccionada en la lista desplegable
        if nameLayer == "" or nameLayer == None:
            return
        selectedLayer = QgsProject.instance().mapLayersByName(nameLayer)[0] #Se selecciona la capa de la base de datos "layers" según el índice
        self.charge_attributes(selectedLayer, combo_box_attri)
        return
        
    #Función llamada cuando se da un cambio en comboBox_cap_gradLine. Se encarga a su vez de cambiar el dato en PFAttri
    def changeFluxLines_Grad(self):
        combo_box_attri = self.dlg.PFAttri
        combo_box_attri.clear()
        nameLayer = self.dlg.comboBox_cap_gradLine.currentText()  # Recibe la capa de subestación seleccionada en la lista desplegable
        if nameLayer == "" or nameLayer == None:
            return
        selectedLayer = QgsProject.instance().mapLayersByName(nameLayer)[0] #Se selecciona la capa de la base de datos "layers" según el índice
        self.charge_attributes(selectedLayer, combo_box_attri)
        return
        
    #Función llamada cuando se da un cambio en comboBox_cap_atrib. Se encarga a su vez de cambiar el dato en combo_Atrib1, combo_Atrib2 y combo_Atrib3
    def changeAttrib(self):
        
        self.dlg.combo_Atrib1.clear()
        self.dlg.combo_Atrib2.clear()
        self.dlg.combo_Atrib3.clear()
        
        nameLayer = self.dlg.comboBox_cap_atrib.currentText()  # Recibe la capa de subestación seleccionada en la lista desplegable
        if nameLayer == "" or nameLayer == None:
            return
        selectedLayer = QgsProject.instance().mapLayersByName(nameLayer)[0] #Se selecciona la capa de la base de datos "layers" según el índice
        
        combo_box_attri = self.dlg.combo_Atrib1
        self.charge_attributes(selectedLayer, combo_box_attri)
        
        combo_box_attri = self.dlg.combo_Atrib2
        self.charge_attributes(selectedLayer, combo_box_attri)
        
        combo_box_attri = self.dlg.combo_Atrib3
        self.charge_attributes(selectedLayer, combo_box_attri)
        return
        
    #Función llamada cuando se da un cambio en comboBox_cap_identif. Se encarga a su vez de cambiar el dato en combo_ident1, combo_ident2 y combo_ident3
    def changeIddentify(self):
        
        self.dlg.combo_ident1.clear()
        self.dlg.combo_ident2.clear()
        self.dlg.combo_ident3.clear()
        
        nameLayer = self.dlg.comboBox_cap_identif.currentText()  # Recibe la capa de subestación seleccionada en la lista desplegable
        if nameLayer == "" or nameLayer == None:
            return
        selectedLayer = QgsProject.instance().mapLayersByName(nameLayer)[0] #Se selecciona la capa de la base de datos "layers" según el índice
        
        combo_box_attri = self.dlg.combo_ident1
        self.charge_attributes(selectedLayer, combo_box_attri)
        
        combo_box_attri = self.dlg.combo_ident2
        self.charge_attributes(selectedLayer, combo_box_attri)
        
        combo_box_attri = self.dlg.combo_ident3
        self.charge_attributes(selectedLayer, combo_box_attri)
        return
    
    def VoltCateg(self):
        
     ########################Codigo para realizar la clasificacion individualizada de los simbolos en la capa de puntos
        
        
        # IndexLayer = self.dlg.comboBox_CR.currentIndex()
        # #selectedLayer = layers[IndexLayer]
        #selectedLayer = iface.activeLayer()
        
        nameLayer = self.dlg.comboBox_cap_categ_tension.currentText()  # Recibe la capa de subestación seleccionada en la lista desplegable
        
        if nameLayer == "" or nameLayer == None:
            aviso = "Seleccione una capa válida"
            QMessageBox.warning(None, QCoreApplication.translate('dialog', "Error"), aviso)
            return
        
        
        selectedLayer = QgsProject.instance().mapLayersByName(nameLayer)[0] #Se selecciona la capa de la base de datos "layers" según el índice de layer_list
        datosLayer = selectedLayer.getFeatures()
        
        # prop =selectedLayer.dataProvider()
        # attr_list = []
        # fields= prop.fields()
        # for field in fields:
            # attr_list.append(field.name())
        
        # self.dlg.ColorRampAttri.addItems(attr_list)
        # expression = self.dlg.ColorRampAttri.currentText()
                            
                        
        #if IndexLayer != 0: #Se verifica que en la IndexLayer se haya elegido una capa
        
        layer = selectedLayer
            
        # Es definido values cuyo formato es: label, lower value, upper value, color name
        # para la identificación dentro de 'MaxV' (uno de los atributos de la tabla) 
                    
                    
        # VL = self.dlg.lineVL.text()
        # if not VL:
            # VL = '0, 114.9'
        # VL=map(float, VL.split(","))
        L = self.dlg.lineL.text()
        if not L:
            L = '0, 0.9499'
        L=list(map(float, L.split(",")))    
        O = self.dlg.lineO.text()
        if not O:
            O = '0.95, 1.0499'
        O=list(map(float, O.split(",")))        
        H = self.dlg.lineH.text()
        if not H:
            H = '1.05, 6'
        H=list(map(float, H.split(",")))            
        
        #Análisis de rangos categorización
        
        try:
            l_inf = float( L[0] )
            l_inf_r = round(l_inf, 2)
            
            l_sup = float( L[1] )
            l_sup_r = round(l_sup, 2)
            
            o_inf = float( O[0] )
            o_inf_r = round(o_inf, 2)
            
            o_sup = float( O[1] )
            o_sup_r = round(o_sup, 2)
            
            h_inf = float( H[0] )
            h_inf_r = round(h_inf, 2)
            
            h_sup = float( H[1] )
            h_sup_r = round(h_sup, 2)
        
        except:
            self.print_error()
            aviso = "Se deben ingresar números válidos en los rangos"
            QMessageBox.warning(None, "Error categorizado tensiones", aviso)
            return
            
        #Rangos correctos
        if l_inf_r > l_sup_r:
            aviso = "El valor inferior de tensión baja debe ser menor al valor superior."
            QMessageBox.warning(None, "Error categorizado tensiones", aviso)
            return
            
        if o_inf_r > o_sup_r:
            aviso = "El valor inferior de tensión óptima debe ser menor al valor superior."
            QMessageBox.warning(None, "Error categorizado tensiones", aviso)
            return
            
        if h_inf_r > h_sup_r:
            aviso = "El valor inferior de tensión alta debe ser menor al valor superior."
            QMessageBox.warning(None, "Error categorizado tensiones", aviso)
            return
            
        if l_sup > o_inf:
            aviso = "El valor superior de tensión baja debe ser menor al valor inferior de tensión óptima."
            QMessageBox.warning(None, "Error categorizado tensiones", aviso)
            return
        
        if o_sup > h_inf:
            aviso = "El valor superior de tensión óptima debe ser menor al valor inferior de tensión alta."
            QMessageBox.warning(None, "Error categorizado tensiones", aviso)
            return
        
        #Que no haya espacios entre rangos
        if l_sup_r != o_inf_r or l_sup == o_inf:
            aviso = "El rango de tensión baja debe ser continuo con respecto al rango de tensión óptima."
            QMessageBox.warning(None, "Error categorizado tensiones", aviso)
            return
            
        if o_sup_r != h_inf_r or o_sup == h_inf:
            aviso = "El rango de tensión óptima debe ser continuo con respecto al rango de tensión alta."
            QMessageBox.warning(None, "Error categorizado tensiones", aviso)
            return
        
        
        # VH = self.dlg.lineVH.text()
        # if not VH:
             # VH = '127,160'
        # VH=map(float, VH.split(","))                
        
        values = (
            #('VeryLow', VL[0], VL[1], 'purple'), Below 0.95 pu
            ('Tension Baja', L[0], L[1], 'orange', 1.7),
            ('Aceptable', O[0], O[1], 'cyan', 2),
            ('Tension Alta', H[0], H[1], 'red', 2.7),
            #('VeryHigh', VH[0], VH[1], 'red'), Above 1.05 pu  Between 0.95 pu and 1.05 pu
            )

        # se crea una rampa graduada segun los valores en values
        ranges = []
                            
        for label, lower, upper, color, size in values:
            symbol = QgsSymbol.defaultSymbol(layer.geometryType()) #inicializa el symbol con valores default
            symbol.setColor(QColor(color)) #Se le asigna un color segun el diccionario "values"
            try:
                symbol.setSize(size)
            except:
                aviso = "Se debe seleccionar una capa que sea del tipo punto"
                QMessageBox.warning(None, "Error categorizado tensiones", aviso)
                return
            
            rng = QgsRendererRange(lower, upper, symbol, label) #Se almacena el diccionario para que sea reconocido como el rango para render
            ranges.append(rng)

        # se crea el render y se le asigna a la capa escogida por el usuario 
        #expression = self.dlg.ColorRampAttri.currentIndex()
        expression = self.dlg.ColorRampAttri.currentText()
        if self.dlg.ColorRampAttri.currentIndex() == 0: #if not expression:
            expression = 'V0' # Atributo base para el renderizado
        
        renderer = QgsGraduatedSymbolRenderer(expression, ranges) #se ejecuta el render graduado basandose en el atributo y segun el rango de colores
        layer.setRenderer(renderer)

        self.iface.mapCanvas().refresh() # se ejecuta un refrescado de las propiedades de la capa
        layer.triggerRepaint() #Activa los cambios inmediatamente al finalizar el plugin
        
        iface.messageBar().pushMessage("Finalizado", "Caractegorización de tensiones finalizada", level=Qgis.Success, duration=3)
       
                 
    def  linesGradua(self):
        
        #####################Codigo para realizar el categorizado de las capas de lineas por su flujo de potencia
         
         nameLayer = self.dlg.comboBox_cap_gradLine.currentText()  # Recibe la capa de subestación seleccionada en la lista desplegable
        
         if nameLayer == "" or nameLayer == None:
             aviso = "Seleccione una capa válida"
             QMessageBox.warning(None, "Error", aviso)
             return
        
        
         selectedLayer = QgsProject.instance().mapLayersByName(nameLayer)[0] #Se selecciona la capa de la base de datos "layers" según el índice
         datosLayer = selectedLayer.getFeatures()
            
         values = (
         ('Por debajo de 80%', 0, 0.7999, 'black', 0.25),
         ('Sobre 80% Abajo de 100%', 0.8, 0.9999, '#e99400', 0.7),
         ('Sobre 100% Abajo de 130%', 1, 1.2999, 'red', 1.1),
         ('Sobre 130%', 1.3, 8, 'red', 1.8),
         )
         #if IndexLayer != 0: #Se verifica que en la IndexLayer se haya elegido una capa
         ranges = []
           
         for label, lower, upper, color, width in values:
             symbol = QgsSymbol.defaultSymbol(selectedLayer.geometryType())
             symbol.setColor(QColor(color))
             symbol = QgsLineSymbol.defaultSymbol(selectedLayer.geometryType())
             try:
                 symbol.setWidth(width)
             except:
                 aviso = "Se debe seleccionar una capa que sea del tipo línea"
                 QMessageBox.warning(None, "Error graduado de líneas", aviso)
                 return
             rng = QgsRendererRange(lower, upper, symbol, label)
             ranges.append(rng)

          
         # create the renderer and assign it to a layer (in this case the actual layer is the chossen by the user)
         expressionPF = self.dlg.PFAttri.currentText()
         if self.dlg.PFAttri.currentIndex() == 0: #if not expression:
             pass # No ejecuta nada ya que no se escogío
         
        
         GraduatedSize = QgsGraduatedSymbolRenderer.setGraduatedMethod
         renderer = QgsGraduatedSymbolRenderer(expressionPF, ranges)
         selectedLayer.setRenderer(renderer)    
         iface.mapCanvas().refresh() # se ejecuta un refrescado de las propiedades de la capa
         selectedLayer.triggerRepaint() #Activa los cambios inmediatamente al finalizar el plugin
         
         iface.messageBar().pushMessage("Finalizado", "Graduación de líneas en conductores finalizada", level=Qgis.Success, duration=3)
      
    def categTx(self):
    
        #####################Codigo para realizar el categorizado de los puntos segun su cargabilidad
         
         nameLayer = self.dlg.comboBox_cap_catTraf.currentText()  # Recibe la capa de subestación seleccionada en la lista desplegable
        
         if nameLayer == "" or nameLayer == None:
             aviso = "Seleccione una capa válida"
             QMessageBox.warning(None, "Error", aviso)
             return
        
        
         selectedLayer = QgsProject.instance().mapLayersByName(nameLayer)[0] #Se selecciona la capa de la base de datos "layers" según e
         datosLayer = selectedLayer.getFeatures()
         
         values = (
         ('Por debajo de 80%', 0, 0.7999, 'black', 1.7),
         ('Sobre 80% Abajo de 100%', 0.8, 0.9999, '#e99400', 1.9),
         ('Sobre 100% Abajo de 130%', 1, 1.2999, 'red', 2.3),
         ('Sobre 130%', 1.3, 8, 'red', 2.7),
         )
         #if IndexLayer != 0: #Se verifica que en la IndexLayer se haya elegido una capa
         ranges = []
                            
         for label, lower, upper, color, size in values:
            symbol = QgsSymbol.defaultSymbol(selectedLayer.geometryType()) #inicializa el symbol con valores default
            symbol.setColor(QColor(color)) #Se le asigna un color segun el diccionario "values"
            try:
                symbol.setSize(size)
            except:
                aviso = "Se debe seleccionar una capa que sea del tipo punto"
                QMessageBox.warning(None, "Error categorizado Tx", aviso)
                return
            symbol.setSize(size)
            rng = QgsRendererRange(lower, upper, symbol, label) #Se almacena el diccionario para que sea reconocido como el rango para render
            ranges.append(rng)
          
         # create the renderer and assign it to a layer (in this case the actual layer is the chossen by the user)
         
         expressionLoad = self.dlg.TxLoad.currentText()
         if self.dlg.TxLoad.currentIndex() == 0: #if not expression:
             pass # No ejecuta nada ya que no se escogío
         
         renderer = QgsGraduatedSymbolRenderer(expressionLoad, ranges) #se ejecuta el render graduado basandose en el atributo y segun el rango de colores
         selectedLayer.setRenderer(renderer)
         self.iface.mapCanvas().refresh() # se ejecuta un refrescado de las propiedades de la capa
         selectedLayer.triggerRepaint() #Activa los cambios inmediatamente al finalizar el plugin
         
         iface.messageBar().pushMessage("Finalizado", "Categorización de transformadores finalizada", level=Qgis.Success, duration=3)

            
    """
    Función que se encarga de asignar los pesos para realizar el mapa de calor
    
    Parámetros de entrada:
    *layer : capa en la que se va a hacer el mapa de calor.
    *selectedAttribute (string): nombre del atributo al que se le va a realizar el mapa de calor.
    
    Valores retornados:
    *0 si hay errores
    *1 si se finalizó correctamente
    """
    def WeightHeatMap(self, layer, selectedAttribute):
        try:
            #Se agrega el atributo weight si no existe en la capa respectiva
            names = layer.dataProvider().fields().names()
            if "weight" not in names:
                weight = layer.dataProvider().addAttributes([QgsField("weight", QVariant.String)])
                layer.updateFields()
                
            #Se analiza línea a línea la capa y se agrega el peso correspondiente
            lines = layer.getFeatures()
            layer.startEditing()
            
            for line in lines:
                value = line[ selectedAttribute ]
                try:
                    value = float( value )
                except:
                    self.print_error()
                    mensaje = str( "Debe seleccionar un atributo con valores numéricos para el mapa de calor")
                    QMessageBox.critical(None, "VISION error heatmap", mensaje)
                    return 0
                #Se asigna un peso equivalente, considerando que lo que se buscan son problemas de tensiones (por tanto si 0.95 < dato < 1.05 no se consideran problemas de tensión)
                if value < 1.05 and value > 0.95:
                    peso = 0
                else:
                    peso = abs( 1 - value ) #Debido a que la tensión nominal representa un value = 1
                
                idx_weight = line.fieldNameIndex("weight")
                layer.changeAttributeValue( line.id(), idx_weight, peso)
            
            layer.commitChanges()
            return 1
        except:
            self.print_error()
            mensaje = str( "Hubo un error al realizar un mapa de calor. Para más información revise la consola.")
            QMessageBox.critical(None,"VISION error heatmap", mensaje)
            return 0
    
    def Hotest(self):
        ######################################################Codigo para realizar los heatmaps en capas de puntos
        
        nameLayer = self.dlg.comboBox_cap_heatmap.currentText()  # Recibe la capa de subestación seleccionada en la lista desplegable
        
        if nameLayer == "" or nameLayer == None:
            aviso = "Seleccione una capa válida"
            QMessageBox.warning(None, "Error", aviso)
            return        
        
        #Lectura de datos del usuario
        selectedLayer = QgsProject.instance().mapLayersByName(nameLayer)[0] #Se selecciona la capa de la base de datos "layers" según el índice
        # create the renderer and assign it to a layer (in this case the actual layer is the chossen by the user)
        attribute = self.dlg.HeatmapAttri.currentText() # attribute name to be classified
        if self.dlg.HeatmapAttri.currentIndex() == 0: #if not expression:
            attribute = 'V0' # Atributo base para el renderizado
        
        #Se llama a la función que asigna los pesos
        sucessfull = self.WeightHeatMap( selectedLayer, attribute ) 
        attribute = "weight"
        
        #Si no se asignaron los pesos se sale de la función
        if sucessfull == 0:
           return 0
        
        
        ####Heatmap
        properties={'color1':'#eeeee6', 'color2':'#b30000', 'stops' : '0.25;#fda553:0.50;#fc6742:0.75;#e34a33'}
        #Se inicializa el diccionario que contiene la rampa continua de coloracion, cuyo formato es: color inferior,
        #color superior y los pasos (donde se nombra el porcentaje del maximo valor)
        ramp = QgsGradientColorRamp.create(properties)
        # se crea una categoria o rampa con base a las propierties
        
        renderer = QgsHeatmapRenderer() #tipo de renderizado
        renderer.setWeightExpression(attribute) #atributo base para el renderizado
        renderer.setRenderQuality(1)#Se setea la calidad del render (menor numero == mayor calidad)
        renderer.setRadius(4.9) #Setea el radio de agrupamiento dependiendo del zoom
        #renderer.setRadiusUnit(QgsSymbol.'Pixel') #setea el tipo de simbolo a pixel ya que por default se hace por mm
        renderer.setColorRamp(ramp) #
        selectedLayer.setRenderer(renderer)
        iface.mapCanvas().refresh()
        selectedLayer.triggerRepaint()
        
        """
        names = selectedLayer.dataProvider().fields().names()
                
        #Se busca el índice de "weight" para eliminarlo
        idx_weight = -1
        for name in names:
            if name == "weight":
                idx_weight = selectedLayer.dataProvider().fieldNameIndex( name )
                break
        if idx_weight != -1:
            selectedLayer.dataProvider().deleteAttributes( [idx_weight] )
            selectedLayer.updateFields()
        """
        
        iface.messageBar().pushMessage("Finalizado", "Mapa de calor finalizado", level=Qgis.Success, duration=3)
    
    
    def PoiAni(self):
            
        ##################################Codigo para realizar las animaciones del comportamiento diario de una capa de puntos    
        
              
        layers = list( QgsProject.instance().mapLayers().values() )
        IndexLayer = self.dlg.comboBox_AN.currentIndex()
        
        if IndexLayer == 0: #Se verifica que en la IndexLayer se haya elegido una capa:
            aviso = "Seleccione una capa válida"
            QMessageBox.warning(None, "Error", aviso)
            return
        
        else: #Se verifica que en la IndexLayer se haya elegido una capa
            
            selectedLayer = layers[IndexLayer - 1]
            layer = selectedLayer
            
            w = 1440/96  #1440/i #tmuestreo, donde i es la cantidad de columnas de muestras       60*24=1440 minutos del dia

            #El usuario solo puede ingresar hora de 00->24
            Adre = self.dlg.lineAdre.text()

            HDow = self.dlg.lineHDow.text()
            HHig = self.dlg.lineHHig.text()
            
            if HDow == "":
                HDow = 0
            else:
                HDow = int( HDow )
            
            if HHig == "":
                HHig = 24
            else:
                HHig = int( HHig )
            
            MDow = HDow * 60 
            MHig = HHig * 60 

            # if Muser ==0:
            # Xten= 0
            # else:
            XDow = int( MDow/w )
            XHig = int( MHig/w )
            # values = (
                # ('Very Low', 1, 2.999, '#178a3a', 1.2),
                # ('Low', 3, 4.9999, 'purple', 1.5),
                # ('Optimal', 5, 6.9999, 'blue', 1.8),
                # ('High', 7, 8.9999, 'orange', 2.2),
                # ('VeryHigh', 9, 10, 'red', 2.7),
                # )
            values = (
                ('Tension Baja', 0, 0.9499, 'orange', 1.7),
                ('Aceptable', 0.95, 1.0499, 'cyan', 2),
                ('Tension Alta', 1.05, 10, 'red', 2.7),
                )

                
            
                # create a category for each item in values
            ranges = []
            for label, lower, upper, color, size in values:
                symbol = QgsSymbol.defaultSymbol(layer.geometryType())
                symbol.setColor(QColor(color))
                
                try:
                    symbol.setSize(size)
                except:
                    aviso = "Se debe seleccionar una capa que sea del tipo punto"
                    QMessageBox.warning(None, "Error animación de puntos", aviso)
                    return
                
                rng = QgsRendererRange(lower, upper, symbol, label)
                ranges.append(rng)  
                
            Vect = []  #Vector vacio para atributos             
            for i in range(XDow, XHig+1): # range(XDow, XHig+1) range(0, 11)
                atri = 'V'+str(i)
                Vect.append(atri)
            Hora= HDow
            minu = 0        

            qgis.utils.iface.actionShowPythonDialog().trigger() #codigo empleado para desplegar la consola
            qgis.utils.iface.actionShowPythonDialog().trigger()
            
            for item in Vect:
                #for item in atri: #busca en la capa el atributo llamado Tension para realizar la labor con cada item del atributo
                
                        #se realiza el render de la capa de puntos
                        
                    # create the renderer and assign it to a layer (in this case the actual layer is the chossen by the user)
                expression = item # attribute name to be classified
                renderer = QgsGraduatedSymbolRenderer(expression, ranges)
                layer.setRenderer(renderer)
                iface.mapCanvas().refresh()
                layer.triggerRepaint()
                time.sleep(1)
                
                expression = item # attribute name to be classified
                renderer = QgsGraduatedSymbolRenderer(expression, ranges)
                layer.setRenderer(renderer)
                iface.mapCanvas().refresh()
                layer.triggerRepaint()
                #etiq = float(item[7])*1440/96
                #iface.messageBar().pushInfo("INFO", QCoreApplication.translate('menu', "Valores de Tension ")+str(Hora)+':'+str(minu))
                iface.mapCanvas().saveAsImage(str(Adre)+"\Tension"+str(Hora)+"_"+str(minu)+".png",None,"PNG")
                #iface.mapCanvas().saveAsImage("D:\Universidad\l ciclo 2016\Proyecto\Archivos QGIS\PapaEmeritus"+item+".png",None,"PNG")
                if minu==45:
                    Hora+=1
                    minu = 0
                else:
                    minu += 15 
                time.sleep(1)
                #iface.mapCanvas().saveAsImage(Adre+"\tension"+str(Hora)+"_"+str(minu)+".png",None,"PNG")
    
        iface.messageBar().pushMessage("Finalizado", "Animación de puntos finalizada", level=Qgis.Success, duration=3)
     
            
    def LinAni(self):       
        ###################################################################Codigo para animacion de capas de lineas
        layers = list( QgsProject.instance().mapLayers().values() )
        IndexLayer = self.dlg.comboBox_ANL.currentIndex()
        
        if IndexLayer == 0: #Se verifica que en la IndexLayer se haya elegido una capa:
            aviso = "Seleccione una capa válida"
            QMessageBox.warning(None, "Error", aviso)
            return
        
        else:
            selectedLayer = layers[IndexLayer - 1]
            layer = selectedLayer
            
            w = 1440/96  #1440/i #tmuestreo, donde i es la cantidad de columnas de muestras       60*24=1440 minutos del dia

            #El usuario solo puede ingresar hora de 00->24
            AdreL = self.dlg.lineAdreL.text()

            HDow = self.dlg.lineHDowL.text()
            HHig = self.dlg.lineHHigL.text()
            
            if HDow == "":
                HDow = 0
            else:
                HDow = int( HDow )
            
            if HHig == "":
                HHig = 24
            else:
                HHig = int( HHig )
            
            MDow = HDow * 60 
            MHig = HHig * 60

            # if Muser ==0:
            # Xten= 0
            # else:
            XDow = int(MDow/w)
            XHig = int(MHig/w)
            values = (
            ('Por debajo de 80%', 0, 0.7999, 'black', 0.25),
            ('Sobre 80% Abajo de 100%', 0.8, 0.9999, '#e99400', 0.7),
            ('Sobre 100% Abajo de 130%', 1, 1.2999, 'red', 1.1),
            ('Sobre 130%', 1.3, 8, 'red', 1.8),
            )
            
                # create a category for each item in values
            ranges = []
            for label, lower, upper, color, width in values:
                symbol = QgsSymbol.defaultSymbol(selectedLayer.geometryType())
                symbol.setColor(QColor(color))
                #symbol = QgsLineSymbol.defaultSymbol(selectedLayer.geometryType())
                try:
                    symbol.setWidth(width)
                except:
                    aviso = "Se debe seleccionar una capa que sea del tipo línea"
                    QMessageBox.warning(None, "Error animación de líneas", aviso)
                    return
                rng = QgsRendererRange(lower, upper, symbol, label)
                ranges.append(rng)
                
            Vect = []  #Vector vacio para atributos             
            for i in range(XDow, XHig+1): # range(XDow, XHig+1) range(0, 11)
                atri = 'PF'+str(i)
                Vect.append(atri)
            Hora= HDow
            minu = 0        

            qgis.utils.iface.actionShowPythonDialog().trigger() #codigo empleado para desplegar la consola
            qgis.utils.iface.actionShowPythonDialog().trigger()
            
            for item in Vect:
                
                        #se realiza el render de la capa de puntos
                        
                    # create the renderer and assign it to a layer (in this case the actual layer is the chossen by the user)
                expression = item # attribute name to be classified
                GraduatedSize = QgsGraduatedSymbolRenderer.setGraduatedMethod
                renderer = QgsGraduatedSymbolRenderer(expression, ranges)
                selectedLayer.setRenderer(renderer)    
                iface.mapCanvas().refresh() # se ejecuta un refrescado de las propiedades de la capa
                selectedLayer.triggerRepaint() #Activa los cambios inmediatamente al finalizar el plugin
                time.sleep(1)
                
                GraduatedSize = QgsGraduatedSymbolRenderer.setGraduatedMethod
                renderer = QgsGraduatedSymbolRenderer(expression, ranges)
                selectedLayer.setRenderer(renderer)    
                iface.mapCanvas().refresh() # se ejecuta un refrescado de las propiedades de la capa
                selectedLayer.triggerRepaint() #Activa los cambios inmediatamente al finalizar el plugin
                #iface.messageBar().pushInfo("INFO", QCoreApplication.translate('menu', "Flujo de Potencia ")+str(Hora)+':'+str(minu))
                iface.mapCanvas().saveAsImage(str(AdreL)+"\Flujo"+str(Hora)+"_"+str(minu)+".png",None,"PNG")
                if minu==45:
                    Hora+=1
                    minu = 0
                else: 
                    minu += 15 
                time.sleep(1)
                #iface.mapCanvas().saveAsImage(str(AdreL)+"\flujo"+str(Hora)+"_"+str(minu)+".png",None,"PNG")
                #iface.mapCanvas().saveAsImage("D:\Universidad\l ciclo 2016\Proyecto\Archivos QGIS\prueba"+item+".png",None,"PNG")
    
        iface.messageBar().pushMessage("Finalizado", "Animación de líneas finalizada", level=Qgis.Success, duration=3)

    def select_output_folder(self):
        """Método para seleccionar la carpeta de destino"""
        foldername = QFileDialog.getExistingDirectory(self.dlg, QCoreApplication.translate('menu', "Seleccione carpeta de destino "), "",)
        self.dlg.lineAdre.setText(foldername)
        
    def select_output_folderL(self):
        """Método para seleccionar la carpeta de destino"""
        foldername = QFileDialog.getExistingDirectory(self.dlg, QCoreApplication.translate('menu', "Seleccione carpeta de destino "), "",)
        self.dlg.lineAdreL.setText(foldername)        
        
        
    def IdentifyFeatures(self):
        import time
        #0= capas de puntos
        #1= capas de lineas
        
        #activeLayer = qgis.utils.iface.activeLayer()
        activeLayer = iface.activeLayer()
        datosLayer = activeLayer.selectedFeatures()
        
        
        #Si no hay ningún objeto seleccionado
        if datosLayer == []:
            message = "Debe seleccionar algún objeto mediante la herramienta 'seleccionar objetos espaciales'"
            QMessageBox.information(None, "Identificación de características", message)
            return 0
            
        names = activeLayer.dataProvider().fields().names()
        
        for item in datosLayer:
            message = ""
            #Agrega el nombre de las columnas al mensaje
            for name in names:
                message += str( name ) + ": " + str( item[name] ) + "\n"
                
            #Se despliega el mensaje
            QMessageBox.information(None, "Identificación de características", message)
        
        iface.messageBar().pushMessage("Finalizado", "Identificación de características finalizada", level=Qgis.Success, duration = 3)
        return 1
        
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&VISION'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        
    def charge_attributes(self, selectedLayer, combobox_attri):
        try:
            attr_list = []
            prop =selectedLayer.dataProvider()
            fields= prop.fields()
            for field in fields:
                attr_list.append(field.name())
            combobox_attri.addItems(attr_list)
        
        except AttributeError: self.print_error()
            


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        #Carga los nombres de las capas actualmente abiertas y las muestra en las listas desplegables 
        layers = QgsProject.instance().mapLayers().values()
        layer_list = []
        layer_list.append("")
        for layer in layers:
            layer_list.append(layer.name())
        
        self.dlg.comboBox_cap_categ_tension.clear()		
        self.dlg.comboBox_cap_categ_tension.addItems(layer_list)
        
        self.dlg.comboBox_cap_heatmap.clear()		
        self.dlg.comboBox_cap_heatmap.addItems(layer_list)
        
        self.dlg.comboBox_cap_gradLine.clear()		
        self.dlg.comboBox_cap_gradLine.addItems(layer_list)
        
        self.dlg.comboBox_cap_catTraf.clear()		
        self.dlg.comboBox_cap_catTraf.addItems(layer_list)
        
        self.dlg.ColorRampAttri.clear()		
        self.dlg.HeatmapAttri.clear()		
        self.dlg.PFAttri.clear()		
        
        
        try: 
            result = self.dlg.exec_()
        except: 
            self.print_error()
            aviso = "Error al ejecutar VISION. Favor revise la consola para corregir el error."
            QMessageBox.critical(None, QCoreApplication.translate('dialog', "Error"), aviso)
            return
        
    
