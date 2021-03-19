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
# Last Modified Date: 2021-03-19 16:55:02


"""
Display pressed keys the on screen and hide automatically after a timeout.
"""

from __future__ import annotations

import platform
from pathlib import Path

from PySide6.QtCore import QPoint, QRect, Qt, QTimer
from PySide6.QtGui import QAction, QFont, QFontDatabase, QIcon, QScreen
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMenu,
    QSizePolicy,
    QSystemTrayIcon,
)

from keypressed.listener import Listener


class App(QApplication):
    """
    The main application
    """

    _font_file: Path = Path(__file__).parent.parent / Path(
        "assets/fonts/JetBrains Mono Bold Nerd Font Complete{0}.ttf".format(
            " Windows Compatible" if platform.system() == "Windows" else ""
        )
    )

    def __init__(self, logo_file: Path, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setQuitOnLastWindowClosed(False)

        font_id: int = QFontDatabase.addApplicationFont(str(self._font_file))
        self.default_font: str = QFontDatabase.applicationFontFamilies(font_id)[
            0
        ]

        self.window: QMainWindow = QMainWindow()
        self.window.setWindowTitle("Keypressed")
        self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.window.setWindowOpacity(0.5)
        self.place()
        self.setActiveWindow(self.window)

        self.label: QLabel = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont(self.default_font, 32))
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setStyleSheet(
            "background-color: rgb(32, 32, 32); color: white;"
        )
        self.label.setTextFormat(Qt.PlainText)
        self.label.setTextInteractionFlags(Qt.NoTextInteraction)
        self.window.setCentralWidget(self.label)

        self.tray: QSystemTrayIcon = QSystemTrayIcon()
        self.tray.setIcon(QIcon(str(logo_file)))
        self.tray.setVisible(True)

        self.menu: QMenu = QMenu()
        quit_action: QAction = self.menu.addAction("&Quit")
        quit_action.triggered.connect(self.exit_app)
        self.tray.setContextMenu(self.menu)

        self.listener: Listener = Listener()
        self.listener.key_pressed.connect(self.show_keys)

        self.timer: QTimer = QTimer(self)

    def place(self) -> None:
        screen: QScreen = QApplication.primaryScreen()
        rect: QRect = QScreen.availableGeometry(screen)
        width: int = rect.size().width()
        height: int = rect.size().height()
        self.window.resize(width, 0.125 * height)

        geo: QRect = self.window.frameGeometry()
        center: QPoint = rect.center()
        geo.moveCenter(center)
        self.window.move(geo.topLeft().x(), 13 / 16 * height)

    def show_keys(self, key: str) -> None:
        self.label.setText(f"key pressed: {key}")
        self.window.show()
        self.timer.singleShot(3000, self.window.close)

    def run(self) -> None:
        # Run the main Qt loop
        self.listener.start()

    def exit_app(self) -> None:
        self.listener.stop()
        self.quit()
