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
# Last Modified Date: 2021-04-11 15:14:50

"""
Listening in the background, emit a Qt signal when a key was pressed.
"""

from __future__ import annotations

import string
import typing as t

from pynput import keyboard as kbd
from PySide6.QtCore import QThread, Signal

from keypressed.key_syms import is_shift_key, modifier_keys, special_keys


class Listener(QThread):
    """
    A class used to detect which key was pressed, based on the QThread.
    """

    key_pressed: Signal = Signal(str)

    def __init__(self, logger) -> None:
        super().__init__()
        self.kbd_listener = kbd.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        self._combinations: t.Set[kbd.Key] = set()
        self._logger = logger

    def run(self) -> None:
        self.kbd_listener.start()
        self.kbd_listener.wait()

    def stop(self) -> None:
        self.kbd_listener.stop()
        super().quit()

    def on_press(self, key: t.Union[kbd.Key, kbd.KeyCode, None]) -> None:
        key_sym: str = ""
        shift_key: str = ""
        if hasattr(key, "char") or key is kbd.Key.tab:
            for mod_key in self._combinations:
                if is_shift_key(mod_key):
                    key_sym += "{shift_key}"
                    shift_key = special_keys.get(mod_key, "Shift+")
                else:
                    key_sym += special_keys.get(mod_key, f"{mod_key.name}+")
            # Combined keys will raise an unprintable character or a whitespace,
            # so I add an extra checking here.
            if key is kbd.Key.tab:
                key_sym += special_keys.get(key, key.name)
            elif key.char in set(string.printable) - set(string.whitespace):
                times: int = 2 if key.char in "{}" else 1
                if self._combinations.intersection(
                    {kbd.Key.shift, kbd.Key.shift_r}
                ):
                    shift_key = ""
                    key_sym += key.char * times
                else:
                    key_sym += key.char.lower() * times
            else:
                key_sym += chr(key.vk).lower()
            key_sym = key_sym.format(shift_key=shift_key)
        elif key:
            if key in modifier_keys:
                self._combinations.add(key)
            else:
                key_sym = special_keys.get(key, key.name)
        if key_sym:
            self._logger.debug(f"{key_sym} emitted")
            self.key_pressed.emit(key_sym)

    def on_release(self, key: t.Union[kbd.Key, kbd.KeyCode, None]) -> None:
        try:
            self._combinations.remove(key)
        except KeyError:
            self._logger.debug(f"Try to remove {key} from combinations set.")
