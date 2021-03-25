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
# Last Modified Date: 2021-03-25 12:45:04

"""
Special key symbol mappings.
"""

from __future__ import annotations

import platform
import typing as t
from collections import defaultdict

from pynput import keyboard as kbd

# Replace symbols
mod_symbols: t.Dict[str, t.DefaultDict[str, str]] = {
    "alt": defaultdict(lambda: "Alt+"),
    "ctrl": defaultdict(lambda: "Ctrl+"),
    "shift": defaultdict(lambda: "Shift+"),
    "super": defaultdict(lambda: "Super+"),
}
mod_symbols["alt"].update({"Darwin": "\u2325+"})
mod_symbols["ctrl"].update({"Darwin": "\u2303+"})
mod_symbols["shift"].update({"Darwin": "\u21e7+"})
mod_symbols["super"].update(
    {"Windows": "\uf17a +", "Linux": "\uf17c +", "Darwin": "\u2318+"}
)

# Enter and editing keys
enter_and_editing_keys: t.Dict[kbd.Key, str] = {
    kbd.Key.backspace: "\u232b",
    kbd.Key.delete: "\u2326",
    kbd.Key.enter: "\u23ce",
    kbd.Key.insert: "Ins",
}

# Function keys
function_keys: t.Dict[kbd.Key, str] = {
    kbd.Key.f1: "F1",
    kbd.Key.f2: "F2",
    kbd.Key.f3: "F3",
    kbd.Key.f4: "F4",
    kbd.Key.f5: "F5",
    kbd.Key.f6: "F6",
    kbd.Key.f7: "F7",
    kbd.Key.f8: "F8",
    kbd.Key.f9: "F9",
    kbd.Key.f10: "F10",
    kbd.Key.f11: "F11",
    kbd.Key.f12: "F12",
}

# Lock keys
lock_keys: t.Dict[kbd.Key, str] = {
    kbd.Key.caps_lock: "\u21ea",
    kbd.Key.num_lock: "\u21ed",
    kbd.Key.scroll_lock: "ScrLck",
}

# Media keys
media_keys: t.Dict[kbd.Key, str] = {
    kbd.Key.media_next: "\uf048 ",
    kbd.Key.media_play_pause: "\u231f",
    kbd.Key.media_previous: "\uf051 ",
    kbd.Key.media_volume_down: "\uf027 ",
    kbd.Key.media_volume_mute: "\uf026 ",
    kbd.Key.media_volume_up: "\uf028 ",
}

# Modifier keys
system: str = platform.system()
modifier_keys: t.Dict[kbd.Key, str] = {
    kbd.Key.alt: mod_symbols["alt"][system],
    kbd.Key.alt_gr: mod_symbols["alt"][system],
    kbd.Key.alt_l: mod_symbols["alt"][system],
    kbd.Key.alt_r: mod_symbols["alt"][system],
    kbd.Key.cmd: mod_symbols["super"][system],
    kbd.Key.cmd_r: mod_symbols["super"][system],
    kbd.Key.ctrl: mod_symbols["ctrl"][system],
    kbd.Key.ctrl_l: mod_symbols["ctrl"][system],
    kbd.Key.ctrl_r: mod_symbols["ctrl"][system],
    kbd.Key.shift: mod_symbols["shift"][system],
    kbd.Key.shift_r: mod_symbols["shift"][system],
}

# Navigation keys
navigation_keys: t.Dict[kbd.Key, str] = {
    # Arrow keys
    kbd.Key.down: "\u2193",
    kbd.Key.left: "\u2190",
    kbd.Key.right: "\u2192",
    kbd.Key.up: "\u2191",
    # Others
    kbd.Key.end: "End",
    kbd.Key.home: "Home",
    kbd.Key.page_down: "PgDn",
    kbd.Key.page_up: "PgUp",
    kbd.Key.tab: "\u21b9" if system != "Darwin" else "\u21e5",
}

# All special keys
special_keys: t.Dict[kbd.Key, str] = (
    {
        kbd.Key.esc: "Esc",
        kbd.Key.menu: "\u25a4",
        kbd.Key.pause: "Pause",
        kbd.Key.print_screen: "PrtScn",
        kbd.Key.space: "\u2423",
    }
    | enter_and_editing_keys
    | function_keys
    | lock_keys
    | media_keys
    | modifier_keys
    | navigation_keys
)
