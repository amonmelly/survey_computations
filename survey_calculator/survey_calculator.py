# -*- coding: utf-8 -*-
"""
/***************************************************************************
 survey_calculator
                                 A QGIS plugin
 Polar Join Computation
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-03-09
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Jcad
        email                : jcad.contact@jcad
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtWidgets import QAction,QFileDialog,QApplication, QSizePolicy,QButtonGroup, QPushButton, QVBoxLayout, QProgressBar, QWidget,QMessageBox
from qgis.core import QgsProject, Qgis

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .survey_calculator_dialog import survey_calculatorDialog
import os.path
import math


class survey_calculator:
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
            'survey_calculator_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Survey Calculator')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

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
        return QCoreApplication.translate('survey_calculator', message)


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

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/survey_calculator/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Polar Join Computation'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Survey Calculator'),
                action)
            self.iface.removeToolBarIcon(action)


    def join_computation(self,cn,ce):
    	def calculate_bearing(cn,ce):
    		b=math.atan(ce/cn)
    		d=math.degrees(b)
    		if d<0:
    			return(d+180)
    		else:
    			return(d)
    	def d_m_s(bearing):
    		d=int(math.trunc(bearing))
    		m_0=(bearing-d)*60
    		m=int(math.trunc(m_0))
    		s=int(round((m_0-m)*60,0))
    		return(str(d)+'d'+str(m)+'d'+str(s))
    	def distance(cn,ce):
    		e2=ce*ce
    		n2=cn*cn
    		dist=math.sqrt((e2+n2))
    		return(str(round(dist,2)))
    	d=calculate_bearing(cn,ce)
    	dms=d_m_s(d)
    	dist=distance(cn,ce)
    	return(dms,dist)
    def read_join_data(self):
    	y_a=float(self.dlg.point_a_y.text())
    	x_a=float(self.dlg.point_a_x.text())
    	y_b=float(self.dlg.point_b_y.text())
    	x_b=float(self.dlg.point_b_x.text())
    	cn=y_b-y_a
    	ce=x_b-x_a
    	bearing,distance=self.join_computation(cn,ce)
    	self.result_display('join',bearing,distance)
    def clearance(self):
    	self.dlg.point_a_y.clear()
    	self.dlg.point_a_x.clear()
    	self.dlg.point_b_y.clear()
    	self.dlg.point_b_x.clear()
    	self.dlg.result_bearing.clear()
    	self.dlg.result_bearing_2.clear()
    	self.dlg.result_distance.clear()
    	self.dlg.origin_y.clear()
    	self.dlg.origin_x.clear()
    	self.dlg.input_distance.clear()
    	self.dlg.bearing_d.clear()
    	self.dlg.bearing_m.clear()
    	self.dlg.bearing_s.clear()
    	self.dlg.result_y.clear()
    	self.dlg.result_x.clear()
    def result_display(self,t,r1,r2):
    	if t=='polar':
    		self.dlg.result_y.setText(r1)
    		self.dlg.result_x.setText(r2)
    	elif t=='join':
    		bearing=r1.split('d')
    		d_b=int(bearing[0])+(int(bearing[1])/60)+(int(bearing[2])/3600)
    		if d_b<180:
    			back_bearing=d_b+180
    		else:
    			back_bearing=d_b-180
    		d=int(math.trunc(back_bearing))
    		m_0=(back_bearing-d)*60
    		m=int(math.trunc(m_0))
    		s=int(round((m_0-m)*60,0))
    		r3=str(d)+'d'+str(m)+'d'+str(s)
    		self.dlg.result_bearing.setText(r1)
    		self.dlg.result_distance.setText(r2)
    		self.dlg.result_bearing_2.setText(r3)
    def read_polar_data(self):
    	def convert_d_2_decimal(d,m,s):
    		return((((s/60)+m)/60)+d)
    	def return_radians(deg):
    		return(math.radians(deg))
    	origin_y=float(self.dlg.origin_y.text())
    	origin_x=float(self.dlg.origin_x.text())
    	distance=float(self.dlg.input_distance.text())
    	bearing_d=int(self.dlg.bearing_d.text())
    	bearing_m=int(self.dlg.bearing_m.text())
    	bearing_s=int(self.dlg.bearing_s.text())
    	b_bearing=self.dlg.back_bearing.isChecked()
    	f_bearing=self.dlg.forward_bearing.isChecked()
    	deg=convert_d_2_decimal(bearing_d,bearing_m,bearing_s)
    	if b_bearing==True and deg>=180:
    		deg=deg-180
    	elif b_bearing==True and deg<=180:
    		deg=deg+180
    	elif f_bearing==True:
    		deg=deg
    	rad=return_radians(deg)
    	cy=distance*math.cos(rad)
    	cx=distance*math.sin(rad)
    	y=origin_y+cy
    	x=origin_x+cx
    	self.result_display('polar',str(round(y,2)),str(round(x,2)))
    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = survey_calculatorDialog()
            self.dlg.join.clicked.connect(self.read_join_data)
            self.dlg.polar.clicked.connect(self.read_polar_data)
            self.dlg.reset.clicked.connect(self.clearance)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
