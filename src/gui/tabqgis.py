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
import time

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtQuick
from PyQt5 import QtWidgets

from qgis.core import Qgis
from qgis.gui import QgsMessageBar

from snail.src.core import SnailLogger
from snail.src.core import SnailThreadPs
from snail.src.core import SnailSettings


class SnailTabQGIS(QtCore.QObject):

    fake = QtCore.pyqtSignal()
    y_maximum_updated = QtCore.pyqtSignal(int)

    def __init__(self, parent, widget, iface):
        super(SnailTabQGIS, self).__init__()

        self.parent = parent
        self._iface = iface
        self._widget = widget
        self._cpu_values = []
        self._ram_values = []
        self._i = 0
        self._max = 100
        self._y_maximum = 100
        self._cpu_series_id = None
        self._ram_series_id = None
        self._last_time = None
        self._displayed = False

        self._cpu_checkbox = None
        self._ram_checkbox = None
        self._container = None

        self._settings = None
        self.read_settings()
        self.init_gui()

        self._thread = SnailThreadPs()
        self._thread.update.connect(self.update)
        self._thread.start()

    def read_settings(self, settings=None):
        if settings:
            self._settings = settings
        else:
            self._settings = SnailSettings.Snapshot()

        if self._cpu_checkbox:
            name = self._settings.cpu_color
            css = "QCheckBox:indicator:checked{{background-color:{}}}".format(name)
            self._cpu_checkbox.setStyleSheet(css)

        if self._ram_checkbox:
            name = self._settings.ram_color
            css = "QCheckBox:indicator:checked{{background-color:{}}}".format(name)
            self._ram_checkbox.setStyleSheet(css)

        if self._container:
            if not self._settings.display_chart and self._displayed:
                self._widget.mChartLayout.removeWidget(self._container)
                self._widget.mGridLayout.removeWidget(self._cpu_checkbox)
                self._widget.mGridLayout.removeWidget(self._ram_checkbox)

                self._container.hide()
                self._cpu_checkbox.hide()
                self._ram_checkbox.hide()

                self._displayed = False
            elif self._settings.display_chart and not self._displayed:
                self._widget.mChartLayout.addWidget(self._container)
                self._widget.mGridLayout.addWidget(self._cpu_checkbox, 0, 0)
                self._widget.mGridLayout.addWidget(self._ram_checkbox, 2, 0)

                self._container.show()
                self._cpu_checkbox.show()
                self._ram_checkbox.show()

                self._displayed = True

        self.fake.emit()

    def init_gui(self):
        self._cpu_checkbox = QtWidgets.QCheckBox()
        name = self._settings.cpu_color
        css = "QCheckBox:indicator:checked{{background-color:{}}}".format(name)
        self._cpu_checkbox.setStyleSheet(css)
        self._cpu_checkbox.setChecked(True)
        self._cpu_checkbox.stateChanged.connect(self.fake)

        self._ram_checkbox = QtWidgets.QCheckBox()
        name = self._settings.ram_color
        css = "QCheckBox:indicator:checked{{background-color:{}}}".format(name)
        self._ram_checkbox.setStyleSheet(css)
        self._ram_checkbox.setChecked(True)
        self._ram_checkbox.stateChanged.connect(self.fake)

        self._view = QtQuick.QQuickView(self.parent)
        self._view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        self._view.rootContext().setContextProperty("snail", self)

        color = QtGui.QColor(self._settings.background_color)
        self._view.setColor(color)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        qml = os.path.join(dir_path, "qml", "lines.qml")
        self._view.setSource(QtCore.QUrl.fromLocalFile(qml))

        self._container = QtWidgets.QWidget.createWindowContainer(self._view)
        self._container.setMinimumHeight(80)
        layout = self._widget.mChartLayout
        if self._settings.display_chart:
            self._displayed = True
            layout.addWidget(self._container)

            self._widget.mGridLayout.addWidget(self._cpu_checkbox, 0, 0)
            self._widget.mGridLayout.addWidget(self._ram_checkbox, 2, 0)

    @QtCore.pyqtProperty(bool, notify=fake)
    def cpu_visible(self, notify=fake):
        if self._cpu_checkbox:
            return self._cpu_checkbox.isChecked()
        else:
            return True

    @QtCore.pyqtProperty(bool, notify=fake)
    def ram_visible(self, notify=fake):
        if self._ram_checkbox:
            return self._ram_checkbox.isChecked()
        else:
            return True

    @QtCore.pyqtProperty(int, notify=y_maximum_updated)
    def y_maximum(self):
        return self._y_maximum

    @QtCore.pyqtProperty(int, notify=fake)
    def max(self):
        return self._max

    @QtCore.pyqtProperty(QtGui.QColor, notify=fake)
    def cpu_color(self):
        return QtGui.QColor(self._settings.cpu_color)

    @QtCore.pyqtProperty(QtGui.QColor, notify=fake)
    def ram_color(self):
        return QtGui.QColor(self._settings.ram_color)

    @QtCore.pyqtProperty(QtGui.QColor, notify=fake)
    def background_color(self):
        return QtGui.QColor(self._settings.background_color)

    @QtCore.pyqtProperty(QtGui.QColor, notify=fake)
    def axis_color(self):
        return QtGui.QColor(self._settings.axes_color)

    @QtCore.pyqtSlot(QtCore.QObject)
    def set_cpu_series_id(self, id):
        self._cpu_series_id = id

    @QtCore.pyqtSlot(QtCore.QObject)
    def set_ram_series_id(self, id):
        self._ram_series_id = id

    def update(self):
        cpu_percent = self._thread.cpu_percent
        ram_percent = self._thread.ram_percent
        ram_mb = self._thread.ram_mb

        if cpu_percent > self._y_maximum:
            self._y_maximum = cpu_percent
            self.y_maximum_updated.emit(self._y_maximum)

        # update chart
        if self._i == self._max:
            # cpu
            self._cpu_values.pop(0)
            self._cpu_values.append(cpu_percent)

            self._cpu_series_id.removePoints(0, self._i)

            for i in range(0, self._i):
                self._cpu_series_id.append(i, self._cpu_values[i])

            # ram
            self._ram_values.pop(0)
            self._ram_values.append(ram_percent)

            self._ram_series_id.removePoints(0, self._i)

            for i in range(0, self._i):
                self._ram_series_id.append(i, self._ram_values[i])
        else:
            self._cpu_series_id.append(self._i, cpu_percent)
            self._cpu_values.append(cpu_percent)

            self._ram_series_id.append(self._i, ram_percent)
            self._ram_values.append(ram_percent)

            self._i += 1

        # update instantaneous values
        self._widget.mCpu.setText(str(cpu_percent))

        ram_percent = '%s' % float('%.2g' % ram_percent)
        self._widget.mRamPercent.setText(ram_percent)
        self._widget.mRamMb.setText(str(ram_mb))

        # check warning limit
        setting = SnailSettings.System.RamWarning
        if SnailSettings.get(setting, False, bool):
            setting = SnailSettings.System.RamWarningLimit
            limit = SnailSettings.get(setting, 90, int)
            if float(ram_percent) > limit:
                msg = "RAM is above limit ({} %)".format(ram_percent)

                if not self._last_time or (time.time() - self._last_time) > 30:
                    self._iface.messageBar().pushMessage("Snail", msg, Qgis.Warning, 3)
                    self._last_time = time.time()
