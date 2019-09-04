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
__date__ = "2019/08/29"
__email__ = "blottiere.paul@gmail.com"
__license__ = "GPLv3"

import subprocess
import importlib


class SnailDependencies(object):

    def __init__(self):
        self._deps = ["psutil"]

    def check_pip(self):
        available = True

        try:
            import pip
        except ImportError:
            available = False

        return available

    def missing(self):
        missing_deps = []

        for dep in self._deps:
            try:
                importlib.import_module(dep)
            except ModuleNotFoundError:
                missing_deps.append(dep)

        return missing_deps

    def resolve(self, dep):
        error = False
        output = None
        cmd = ["python3", "-m", "pip", "install", dep, "--user"]

        try:
            output = subprocess.check_output(cmd)
        except subprocess.CalledProcessError:
            try:
                importlib.import_module(dep)
            except ModuleNotFoundError:
                error = True

        return [error, ' '.join(cmd), output.decode('utf-8')]
