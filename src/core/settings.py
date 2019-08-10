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
from qgis.core import QgsSettings
from snail.src.core import SnailLogger


class SnailSettings(object):

    class System(enum.Enum):

        DisplayChart = "system/display_chart"
        CpuColor = "system/cpu_color"
        BackgroundColor = "system/background_color"
        AxisColor = "system/axis_color"
        RefreshMs = "system/refresh_ms"


    def get(setting, default, type=str):
        key = "snail/{}".format(setting.value)
        value = QgsSettings().value(key, default)

        SnailLogger.log("{}: {}".format(key, str(value)))

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
