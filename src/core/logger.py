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


from qgis.core import QgsMessageLog


class SnailLogger(object):
    class __SnailLogger:
        def __init__(self):
            self.val = None

        def __str__(self):
            return 'self' + self.val

    instance = None

    def __new__(cls):
        if not Snail.instance:
            Snail.instance = Snail.__Snail()
        return Snail.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)

    def log(msg):
        QgsMessageLog.logMessage(msg, "Snail")
