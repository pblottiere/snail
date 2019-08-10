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

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtQuick
from PyQt5 import QtWidgets

from snail.src.core import SnailLogger
from snail.src.core import SnailThreadPs
from snail.src.core import SnailSettings


class SnailTabSystem(QtCore.QObject):

    def __init__(self, parent, widget):
        super(SnailTabSystem, self).__init__()

        self.parent = parent
        self._widget = widget
        self._values = []
        self._i = 0
        self._max = 100
        self._series_id = None

        self.init_gui()

        self._thread = SnailThreadPs()
        self._thread.update.connect(self.update)
        self._thread.start()

    def init_gui(self):
        self._view = QtQuick.QQuickView(self.parent)
        self._view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        self._view.rootContext().setContextProperty("snail", self)

        setting = SnailSettings.System.BackgroundColor
        color = QtGui.QColor(SnailSettings.get(setting, QtGui.QColor("white")))
        self._view.setColor(color)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        qml = os.path.join(dir_path, "qml", "lines.qml")
        self._view.setSource(QtCore.QUrl.fromLocalFile(qml))

        self._container = QtWidgets.QWidget.createWindowContainer(self._view)
        self._container.setMinimumHeight(50)
        layout = self._widget.mChartLayout
        setting = SnailSettings.System.DisplayChart
        if SnailSettings.get(setting, True, bool):
            layout.addWidget(self._container)

    @QtCore.pyqtProperty(int)
    def max(self):
        return self._max

    @QtCore.pyqtProperty(QtGui.QColor)
    def cpu_color(self):
        setting = SnailSettings.System.CpuColor
        color = SnailSettings.get(setting, QtGui.QColor("blue").name())
        return QtGui.QColor(color)

    @QtCore.pyqtProperty(QtGui.QColor)
    def background_color(self):
        setting = SnailSettings.System.BackgroundColor
        color = SnailSettings.get(setting, QtGui.QColor("white").name())
        return QtGui.QColor(color)

    @QtCore.pyqtProperty(QtGui.QColor)
    def axis_color(self):
        setting = SnailSettings.System.AxisColor
        color = SnailSettings.get(setting, QtGui.QColor("white").name())
        return QtGui.QColor(color)

    @QtCore.pyqtSlot(QtCore.QObject)
    def set_series_id(self, id):
        self._series_id = id

    def update(self):
        percent = self._thread.percent
        series = self._series_id

        # update chart
        if self._i == self._max:
            self._values.pop(0)
            self._values.append(percent)

            series.removePoints(0, self._i)

            for i in range(0, self._i):
                series.append(i, self._values[i])
        else:
            series.append(self._i, percent)
            self._values.append(percent)
            self._i += 1

        # update instantaneous values
        self._widget.mCpu.setText(str(percent))
