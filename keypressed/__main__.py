#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

# MIT License
#
# Copyright (c) 2021 Pagliacii
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Author:             Pagliacii
# Last Modified By:   Pagliacii
# Created Date:       2021-03-15 14:38:05
# Last Modified Date: 2021-03-16 16:41:49


"""
The entry point.
"""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QScreen
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QMainWindow,
    QMenu,
    QSystemTrayIcon,
)


class App(QApplication):
    """
    The main application
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.window: QMainWindow = QMainWindow()
        self.window.setWindowTitle("Keypressed")
        self.window.setWindowFlags(Qt.FramelessWindowHint)
        self.window.setWindowOpacity(0.5)
        self.center()
        self.setActiveWindow(self.window)

        self.frame: QFrame = QFrame()
        self.frame.resize(600, 400)
        self.frame.setStyleSheet("background-color: rgb(32, 32, 32)")
        self.window.setCentralWidget(self.frame)

        self.tray: QSystemTrayIcon = QSystemTrayIcon()
        self.tray.setIcon(QIcon("logo.png"))
        self.tray.setVisible(True)

        self.menu: QMenu = QMenu()
        quit_action: QAction = self.menu.addAction("&Quit")
        quit_action.triggered.connect(self.quit)
        self.tray.setContextMenu(self.menu)

    def center(self) -> None:
        geo = self.window.frameGeometry()
        center = QScreen.availableGeometry(
            QApplication.primaryScreen()
        ).center()
        geo.moveCenter(center)
        self.window.move(geo.topLeft())

    def run(self) -> None:
        # Run the main Qt loop
        self.window.show()
        sys.exit(self.exec_())


if __name__ == "__main__":
    app: App = App(sys.argv)
    app.run()
