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


import enum
from PyQt5 import QtGui
from qgis.core import QgsSettings
from snail.src.core import SnailLogger


class SnailSettings(object):


    class Snapshot(object):

        def __init__(self):
            setting = SnailSettings.System.CpuColor
            name = SnailSettings.get(setting, QtGui.QColor("blue").name())
            self.cpu_color = name

            setting = SnailSettings.System.RamColor
            name = SnailSettings.get(setting, QtGui.QColor("red").name())
            self.ram_color = name

            setting = SnailSettings.System.BackgroundColor
            name = SnailSettings.get(setting, QtGui.QColor("white").name())
            self.background_color = name

            setting = SnailSettings.System.AxisColor
            name = SnailSettings.get(setting, QtGui.QColor("grey").name())
            self.axes_color = name

            setting = SnailSettings.System.DisplayChart
            display = SnailSettings.get(setting, True, bool)
            self.display_chart = display

    class System(enum.Enum):

        DisplayChart = "system/display_chart"
        CpuColor = "system/cpu_color"
        RamColor = "system/ram_color"
        BackgroundColor = "system/background_color"
        AxisColor = "system/axis_color"
        RefreshSec = "system/refresh_sec"
        RamWarning = "system/ram_warning"
        RamWarningLimit = "system/ram_warning_limit"

    def get(setting, default, type=str):
        key = "snail/{}".format(setting.value)
        value = QgsSettings().value(key, default)

        if type==bool:
            if str(value) == "true" or str(value) == "True":
                value = True
            else:
                value = False
        if type==int:
            value = int(value)

        return value

    def set(setting, value):
        key = "snail/{}".format(setting.value)
        QgsSettings().setValue(key, value)
