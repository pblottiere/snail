# -*- coding: utf-8 -*-

"""
QGIS Plugin for monitoring performances.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Paul Blottiere"
__contact__ = "blottiere.paul@gmail.com"
__copyright__ = "Copyright 2019, Paul Blottiere"
__date__ = "2019/07/19"
__email__ = "blottiere.paul@gmail.com"
__license__ = "GPLv3"


from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
import os.path

from .src.core import SnailDependencies
from .src.gui import SnailDependenciesWidget
from .src.gui import SnailDockWidget
from .src.gui import SnailSettingsWidget


class Snail(object):
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
        locale = QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir, "i18n", "Snail_{}.qm".format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > "4.3.3":
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u"&Snail")

        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u"Snail")
        self.toolbar.setObjectName(u"Snail")

        self.pluginIsActive = False
        self._dockwidget = None
        self._settingswidget = None
        self._dependencies_widget = None

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
        return QCoreApplication.translate("Snail", message)

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
        parent=None,
    ):
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
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        deps = SnailDependencies()

        action = self.run
        if deps.missing():
            action = self.dependencies

        icon_path = ":/plugins/snail/snail.png"
        self.add_action(
            icon_path,
            text=self.tr(u"Snail"),
            callback=action,
            parent=self.iface.mainWindow(),
        )

        icon_path = ":/plugins/snail/settings.png"
        action = self.add_action(
            icon_path,
            text=self.tr(u"Settings"),
            callback=self.settings,
            parent=self.iface.mainWindow(),
            add_to_toolbar=False
        )
        action.setEnabled(False)

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        self._dockwidget.closingPlugin.disconnect(self.onClosePlugin)
        self.pluginIsActive = False

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u"&Snail"), action)
            self.iface.removeToolBarIcon(action)

        # remove the toolbar
        del self.toolbar

    def dependencies(self):
        if not self._dependencies_widget:
            self._dependencies_widget = SnailDependenciesWidget()

        self._dependencies_widget.show()

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            self._dockwidget = SnailDockWidget(self.iface)

            # connect to provide cleanup on closing of dockwidget
            self._dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self._dockwidget)

            self._dockwidget.show()

    def settings(self):

        if not self._settingswidget:
            self._settingswidget = SnailSettingsWidget()

        self._settingswidget.show()
