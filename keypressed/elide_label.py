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
# Created Date:       2021-04-10 15:18:29
# Last Modified Date: 2021-04-10 18:46:29

"""
A custom QT Label that can elide long text automatically.
"""

from __future__ import annotations

import typing as t

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QPaintEvent, QTextCursor, QTextDocument
from PySide6.QtWidgets import QLabel, QWidget


class ElideLabel(QLabel):
    """
    A custom QT Label that can elide long text automatically.
    """

    def __init__(
        self,
        text: t.Optional[str] = None,
        parent: t.Optional[QWidget] = None,
        f: Qt.WindowFlags = Qt.WindowFlags(),
        elide_on_left: bool = False,
        elide_mark: str = "...",
    ) -> None:
        if text:
            super().__init__(text, parent=parent, f=f)
        else:
            super().__init__(parent=parent, f=f)
        self._elide_on_left: bool = elide_on_left
        self._elide_mark: str = elide_mark

    def elide_text(self) -> None:
        """
        Elides long rich text.

        Ref: https://stackoverflow.com/a/66412942/6838452
        """
        rich_text: str = self.text()
        doc: QTextDocument = QTextDocument()
        doc.setDocumentMargin(self.font().pixelSize() / 2.0)
        doc.setDefaultFont(self.font())
        doc.setHtml(rich_text)

        doc_width: float = doc.documentLayout().documentSize().width()
        metric: QFontMetrics = QFontMetrics(self.font())
        mark_width: int = metric.horizontalAdvance(self._elide_mark)

        if (width := self.width() - mark_width) > 0 and doc_width > width:
            cursor: QTextCursor = QTextCursor(doc)
            cursor.movePosition(QTextCursor.Start)

            while doc_width > width:
                if self._elide_on_left:
                    cursor.deleteChar()
                else:
                    cursor.deletePreviousChar()
                doc_width = doc.documentLayout().documentSize().width()

            cursor.insertHtml(f"<span>{self._elide_mark}</span>")
            rich_text = doc.toHtml()

        self.setText(rich_text)

    def paintEvent(self, event: QPaintEvent) -> None:
        # pylint: disable=invalid-name
        self.elide_text()
        super().paintEvent(event)
