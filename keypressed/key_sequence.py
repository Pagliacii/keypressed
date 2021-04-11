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
# Created Date:       2021-04-10 17:57:19
# Last Modified Date: 2021-04-11 14:17:36

"""Contains all pressed keys."""

from __future__ import annotations

import typing as t
from functools import partial

from keypressed import default_logger


class KeySequence:
    """
    Contains all pressed keys.
    """

    def __init__(
        self, font_size: int = 16, max_same_key: int = 3, logger=None
    ) -> None:
        self._sequence: t.List[str] = []
        self._last_pressed_key: str = ""
        self._pressed_times: int = 0
        self._additional = partial(self.additional_text, font_size)
        self._max_same_key: int = max_same_key
        self._logger = logger or default_logger

    def __str__(self) -> str:
        return "".join(self._sequence).strip()

    def additional_text(self, size: int, num: int) -> str:
        return f'<span style="font-size: {size}px;">...{num}x</span>'

    def accept(self, key: str) -> None:
        if key != self._last_pressed_key:
            self._last_pressed_key = key
            self._pressed_times = 1
            self._sequence.append(key)
        elif self._pressed_times < self._max_same_key:
            self._pressed_times += 1
            self._sequence.append(key)
        else:
            if self._pressed_times > self._max_same_key:
                self._sequence.pop()
            self._pressed_times += 1
            self._sequence.append(self._additional(self._pressed_times))
        self._logger.debug(
            f"KeySequence = {self}, Last Key = {key}, "
            f"Pressed: {self._pressed_times}"
        )

    def clear(self) -> None:
        self._sequence = []
        self._last_pressed_key = ""
        self._pressed_times = 0
