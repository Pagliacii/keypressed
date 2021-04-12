#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
# Created Date:       2021-04-10 15:00:36
# Last Modified Date: 2021-04-12 18:04:55

"""Contains all utility functions"""

from __future__ import annotations

import platform
import typing as t
from functools import partial

from pynput import keyboard as kbd

if platform.system() == "Windows":
    from ctypes import windll, wintypes

_escape_characters: t.Dict[str, str] = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&apos;",
}


def escape_characters(string: str) -> str:
    """
    Escapes all HTML characters in the string.

    Currently the "&", "<", ">", "\"" and "'" characters will be escaped.

    Args:
        string (str):
            string to be escaped
    Returns:
        An escaped string.
    """
    for char, escape in _escape_characters.items():
        string = string.replace(char, escape)
    return string


def _detect_key(key: kbd.Key, keys: t.Tuple[kbd.Key]) -> bool:
    """
    Detects a key if it in the keys set.

    Args:
        key (pynput.keyboard.Key):
            which key to be detected
    Returns:
        A boolean value to indicate detect result.
    """
    return key in keys


# Modifier key detect functions
is_alt_key = partial(
    _detect_key,
    keys=(kbd.Key.alt, kbd.Key.alt_gr, kbd.Key.alt_l, kbd.Key.alt_r),
)
is_ctrl_key = partial(
    _detect_key, keys=(kbd.Key.ctrl, kbd.Key.ctrl_l, kbd.Key.ctrl_r)
)
is_shift_key = partial(_detect_key, keys=(kbd.Key.shift, kbd.Key.shift_l))
is_super_key = partial(_detect_key, keys=(kbd.Key.cmd, kbd.Key.cmd_r))


def char_from_vk(vk: int) -> str:
    """
    Converts the virtual key code to a character by using MapVirtualKeyW.

    Notes:
        MapVirtualKeyW is a Windows API.
        Details: https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mapvirtualkeyw

    Args:
        vk (int):
            A virtual key code.
    Returns:
        A single character of the key.
    """  # pylint: disable=line-too-long
    if platform.system() != "Windows":
        return chr(vk)

    # pylint: disable=invalid-name
    MAPVK_VK_TO_CHAR = 2
    MapVirtualKeyW = windll.user32.MapVirtualKeyW
    MapVirtualKeyW.argtypes = (wintypes.UINT, wintypes.UINT)
    MapVirtualKeyW.restype = wintypes.UINT
    return chr(MapVirtualKeyW(vk, MAPVK_VK_TO_CHAR))
