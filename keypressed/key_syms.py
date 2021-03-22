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
# Created Date:       2021-03-17 22:06:42
# Last Modified Date: 2021-03-22 18:14:44

"""
Special key symbol mappings.
"""

from __future__ import annotations

import platform
import typing as t

from pynput import keyboard as kbd

ctrl_key: str = "⌘+" if platform.system() == "Darwin" else "Ctrl+"
special_keys: t.Dict[kbd.Key, str] = {
    kbd.Key.backspace: "⌫",
    kbd.Key.esc: "Esc",
    kbd.Key.space: "␣",
    kbd.Key.ctrl: ctrl_key,
    kbd.Key.ctrl_l: ctrl_key,
    kbd.Key.ctrl_r: ctrl_key,
}
modifier_keys: t.Set[kbd.Key] = {
    kbd.Key.alt,
    kbd.Key.alt_gr,
    kbd.Key.alt_l,
    kbd.Key.alt_r,
    kbd.Key.cmd,
    kbd.Key.cmd_r,
    kbd.Key.ctrl,
    kbd.Key.ctrl_l,
    kbd.Key.ctrl_r,
    kbd.Key.shift,
    kbd.Key.shift_r,
}
