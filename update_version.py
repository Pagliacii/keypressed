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
# Created Date:       2021-08-01 10:21:06
# Last Modified Date: 2021-08-01 10:54:52

import re
from pathlib import Path

import toml

# Prepares
metadata = toml.load(Path.cwd() / "pyproject.toml")
version = metadata["tool"]["poetry"]["version"]

# Updates
init_file = Path.cwd() / "keypressed/__init__.py"
text = init_file.read_text()
updated_text = re.sub(
    r'^(?P<prefix>__version__ = "keypressed )(\d\.\d\.\d)(?P<suffix>")$',
    rf"\g<prefix>{version}\g<suffix>",
    text,
    flags=re.M,
)
init_file.write_text(updated_text)
print("\N{Party Popper} Version updated!!!")
