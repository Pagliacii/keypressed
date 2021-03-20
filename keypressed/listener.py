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
# Created Date:       2021-03-17 22:05:17
# Last Modified Date: 2021-03-20 14:05:24

"""
Listening in the background, emit a Qt signal when a key was pressed.
"""

from __future__ import annotations

import typing as t

from pynput import keyboard as kbd
from PySide6.QtCore import QThread, Signal

from keypressed.key_syms import special_keys


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
            self.key_pressed.emit(special_keys.get(key, key))
