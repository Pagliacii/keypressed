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
# Last Modified Date: 2021-04-11 14:17:19


"""
Display pressed keys the on screen and hide automatically after a timeout.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, QPoint, QRect, Qt, QTimer
from PySide6.QtGui import QAction, QFont, QFontDatabase, QIcon, QScreen
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QSizePolicy,
    QSystemTrayIcon,
)

from keypressed import default_logger
from keypressed.elide_label import ElideLabel
from keypressed.key_sequence import KeySequence
from keypressed.listener import Listener
from keypressed.utils import escape_characters


class Fonts(QObject):
    """
    Appends custom fonts.
    """

    _fonts_dir: Path = Path(__file__).parent.parent / Path("assets/fonts")
    _loaded: bool = False

    @classmethod
    def load_fonts(cls) -> None:
        if not QApplication.instance():
            return
        if not cls._fonts_dir.exists():
            return

        for font_file in cls._fonts_dir.iterdir():
            if font_file.suffix not in (".ttf", ".otf"):
                continue
            QFontDatabase.addApplicationFont(str(font_file))
        cls._loaded = True

    @classmethod
    def font(cls, font_family: str, font_size: int) -> QFont:
        if not cls._loaded:
            cls.load_fonts()
        font = QFont(font_family)
        font.setPixelSize(font_size)
        return font


class App(QApplication):
    """
    The main application
    """

    def __init__(
        self,
        logo_file: Path,
        *args,
        background_color: str = "#202020",
        font_color: str = "white",
        font_family: str = "JetBrainsMono Nerd Font Bold",
        font_size: int = 64,
        margin: int = 8,
        opacity: float = 0.5,
        timeout: int = 3000,
        title: str = "Keypressed",
        logger=None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._logger = logger or default_logger
        self.setQuitOnLastWindowClosed(False)

        self.title: str = title
        self.window: QMainWindow = QMainWindow()
        self.window.setWindowTitle(self.title)
        self.window.setWindowFlags(
            Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint
        )
        self.window.setWindowOpacity(opacity)
        self.setActiveWindow(self.window)

        self.font: QFont = Fonts.font(font_family, font_size)
        self.font.setWeight(QFont.Bold)
        self.label: ElideLabel = ElideLabel(elide_on_left=True)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setFont(self.font)
        self.label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.label.setStyleSheet(
            f"background-color: {background_color}; color: {font_color};"
        )
        self.label.setTextFormat(Qt.RichText)
        self.label.setTextInteractionFlags(Qt.NoTextInteraction)
        self.label.setMargin(margin)
        self.window.setCentralWidget(self.label)

        self.place()

        self.tray: QSystemTrayIcon = QSystemTrayIcon()
        self.tray.setIcon(QIcon(str(logo_file)))
        self.tray.setVisible(True)

        self.menu: QMenu = QMenu()
        quit_action: QAction = self.menu.addAction("&Quit")
        quit_action.triggered.connect(self.exit_app)
        self.tray.setContextMenu(self.menu)

        self.listener: Listener = Listener(self._logger)
        self.listener.key_pressed.connect(self.show_keys)

        self.timer: QTimer = QTimer(self)
        self.timer.setInterval(timeout)
        self.timer.timeout.connect(self.handle_timeout)

        self._sequence: KeySequence = KeySequence(
            font_size=font_size // 2, logger=self._logger
        )

    def place(self) -> None:
        screen: QScreen = QApplication.primaryScreen()
        rect: QRect = QScreen.availableGeometry(screen)
        width: int = rect.size().width()
        height: int = rect.size().height()
        self.window.setFixedSize(width, 0.125 * height)
        self.label.setFixedSize(width, 0.125 * height)

        geo: QRect = self.window.frameGeometry()
        center: QPoint = rect.center()
        geo.moveCenter(center)
        self.window.move(geo.topLeft().x(), 13 / 16 * height)

    def show_keys(self, key: str) -> None:
        self._sequence.accept(escape_characters(key))
        self.label.clear()
        self.label.setText(str(self._sequence))
        self._logger.debug(f"Label: {self.label.text()}")
        self.window.setVisible(True)
        self.timer.start()

    def run(self) -> None:
        # Run the main Qt loop
        self._logger.info("Starting...")
        self.listener.start()
        self._logger.info("Running...")

    def exit_app(self) -> None:
        self._logger.info("See ya!")
        self.listener.stop()
        self.quit()

    def handle_timeout(self) -> None:
        self.label.clear()
        self._sequence.clear()
        QTimer.singleShot(10, lambda: self.window.setVisible(False))
        if self.timer.isActive():
            self.timer.stop()
