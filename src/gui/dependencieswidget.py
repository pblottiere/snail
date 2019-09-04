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
__date__ = "2019/08/31"
__email__ = "blottiere.paul@gmail.com"
__license__ = "GPLv3"


import os
from PyQt5 import QtCore, QtWidgets, uic
from snail.src.core import SnailDependencies


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/dependencies.ui'))

class SnailDependenciesWidget(QtWidgets.QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self._init_gui()
        self.mYes.clicked.connect(self._yes)
        self.mClose.clicked.connect(self.close)

    def _init_gui(self):
        self.mProgress.setValue(0)
        for dep in SnailDependencies().missing():
            self.mMissing.addItem(dep)

    def _yes(self):
        deps = SnailDependencies()
        missing = deps.missing()

        self.mClose.setEnabled(False)
        self.mYes.setEnabled(False)

        self.mProgress.setRange(0, 100)
        self.mProgress.setValue(0)
        step = 100/len(missing)

        text = '<html>'
        err = False
        if deps.check_pip():
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            for dep in missing:
                error, cmd, output = deps.resolve(dep)
                err |= error

                text += '<b>$ {}</b><br/>{}'.format(cmd, output)
                text.replace('\\n', '<br/>')

                value = self.mProgress.value()
                self.mProgress.setValue(value+step)
            QtWidgets.QApplication.restoreOverrideCursor()
        else:
            text += ('<b>Error</b>: \'pip\' Python module is not'
                     ' installed so dependencies cannot be automatically '
                     'resolved.')
            err = True

        if not err:
            text += ('<br/><br/><b>Dependencies have been installed with success. '
                     'You have to restart QGIS now.</b>')
        else:
            text += ('<br/><br/><b>Dependencies failed to resolve. Snail'
                     ' plugin cannot be use for now.</b>')

        text += '</html>'
        self.mLog.setText(text)

        max = self.mLog.verticalScrollBar().maximum()
        self.mLog.verticalScrollBar().setValue(max)

        self.mClose.setEnabled(True)
