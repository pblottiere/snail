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
import psutil as ps
from threading import Thread

from PyQt5 import QtCore

from .logger import SnailLogger
from .settings import SnailSettings


class SnailThreadPs(QtCore.QObject, Thread):

    update = QtCore.pyqtSignal()

    def __init__(self):
        super(QtCore.QObject, self).__init__()
        super(Thread, self).__init__()
        self.cpu_percent = 0
        self.ram_percent = 0
        self.ram_mb = 0

        setting = SnailSettings.System.RefreshMs
        self._period_ms = SnailSettings.get(setting, 500, int)/1000

    def run(self):
        while True:
            qgis_app = ps.Process(os.getpid())
            self.cpu_percent = qgis_app.cpu_percent(interval=1)
            self.ram_percent = qgis_app.memory_percent(memtype="rss")
            self.ram_mb = qgis_app.memory_info()[0] >> 20
            self.update.emit()

            time.sleep(self._period_ms)
