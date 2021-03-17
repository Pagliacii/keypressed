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
# Last Modified Date: 2021-03-17 16:25:27


"""
Display pressed keys the on screen and hide automatically after a timeout.
"""

from __future__ import annotations

import sys
import typing as t

from pynput import keyboard as kbd
from PySide6.QtCore import QPoint, QRect, Qt, QThread, Signal
from PySide6.QtGui import QAction, QIcon, QScreen
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMenu,
    QSystemTrayIcon,
)

special_keys: t.Dict[kbd.Key, str] = {
    kbd.Key.backspace: "⌫",
    kbd.Key.esc: "Esc",
    kbd.Key.space: "␣",
}


class Listener(QThread):
    """
    A class used to detect which key was pressed, based on the QThread.
    """

    key_pressed: Signal = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.kbd_listener = kbd.Listener(on_press=self.on_press)

    def run(self) -> None:
        self.kbd_listener.start()
        self.kbd_listener.wait()

    def stop(self) -> None:
        self.kbd_listener.stop()
        super().quit()

    def on_press(self, key: t.Union[kbd.Key, kbd.KeyCode, None]) -> None:
        if hasattr(key, "char"):
            self.key_pressed.emit(key.char)
        elif key is not None:
            self.key_pressed.emit(special_keys[key])


class App(QApplication):
    """
    The main application
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.window: QMainWindow = QMainWindow()
        self.window.setWindowTitle("Keypressed")
        self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.window.setWindowOpacity(0.5)
        self.place()
        self.setActiveWindow(self.window)

        self.label: QLabel = QLabel()
        self.label.setTextInteractionFlags(Qt.NoTextInteraction)
        self.label.setStyleSheet("background-color: rgb(32, 32, 32)")
        self.window.setCentralWidget(self.label)

        self.tray: QSystemTrayIcon = QSystemTrayIcon()
        self.tray.setIcon(QIcon("logo.png"))
        self.tray.setVisible(True)

        self.menu: QMenu = QMenu()
        quit_action: QAction = self.menu.addAction("&Quit")
        quit_action.triggered.connect(self.exit_app)
        self.tray.setContextMenu(self.menu)

        self.listener: Listener = Listener()
        self.listener.key_pressed.connect(self.show_keys)

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
        print(f"{key=}")

    def run(self) -> None:
        # Run the main Qt loop
        self.listener.start()
        sys.exit(self.exec_())

    def exit_app(self) -> None:
        self.listener.stop()
        self.quit()


if __name__ == "__main__":
    app: App = App(sys.argv)
    app.run()
