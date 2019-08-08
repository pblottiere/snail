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


import psutil as ps
import time
from threading import Thread

from PyQt5 import QtCore

from .logger import SnailLogger


class SnailThreadPs(QtCore.QObject, Thread):

    update = QtCore.pyqtSignal()

    def __init__(self):
        super(QtCore.QObject, self).__init__()
        super(Thread, self).__init__()
        self.percent = 0

    def run(self):
        while True:
            SnailLogger.log("RUN!!")
            time.sleep(4)

            percents = ps.cpu_percent(interval=1, percpu=True)
            self.percent = percents[0]

            self.update.emit()