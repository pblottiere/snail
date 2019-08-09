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


import os
from PyQt5 import QtWidgets, QtCore, uic, QtGui
from qgis.gui import QgsColorButton
from snail.src.core import SnailSettings

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/settingswidget.ui'))


class SnailTabSettingsSystem(QtCore.QObject):

    def __init__(self, parent, widget):
        super(SnailTabSettingsSystem, self).__init__()

        self.parent = parent
        self._widget = widget

        self.init_gui()

    def init_gui(self):
        setting = SnailSettings.System.DisplayChart
        display_chart = SnailSettings.get(setting, True, bool)
        checkbox = self._widget.mSystemDisplayChart
        checkbox.setChecked(display_chart)

        setting = SnailSettings.System.CpuColor
        color = SnailSettings.get(setting, QtGui.QColor("blue"))
        self._cpu_color = QgsColorButton()
        self._cpu_color.setColor(QtGui.QColor(color))
        self._widget.mCpuLayout.addWidget(self._cpu_color)

        self._ram_color = QgsColorButton()
        self._widget.mRamLayout.addWidget(self._ram_color)

        setting = SnailSettings.System.BackgroundColor
        color = SnailSettings.get(setting, QtGui.QColor("white"))
        self._background_color = QgsColorButton()
        self._background_color.setColor(QtGui.QColor(color))
        self._widget.mBackgroundLayout.addWidget(self._background_color)

        self._axes_color = QgsColorButton()
        self._widget.mAxesLayout.addWidget(self._axes_color)

    def store(self):
        checkbox = self._widget.mSystemDisplayChart
        setting = SnailSettings.System.DisplayChart
        SnailSettings.set(setting, checkbox.isChecked())

        cpu_color = self._cpu_color.color().name()
        setting = SnailSettings.System.CpuColor
        SnailSettings.set(setting, cpu_color)

        background_color = self._background_color.color().name()
        setting = SnailSettings.System.BackgroundColor
        SnailSettings.set(setting, background_color)


class SnailSettingsWidget(QtWidgets.QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self._tab_system = SnailTabSettingsSystem(parent, self)

    def accept(self):
        self._tab_system.store()
        self.close()
