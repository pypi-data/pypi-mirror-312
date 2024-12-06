# -*- mode: python -*-
# vi: set ft=python :

# Copyright (C) 2024 The C++ Plus Project.
# This file is part of the Rubisco.
#
# Rubisco is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# Rubisco is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Rubisco exceptions definitions.

These exceptions is used to describe a exception that has a document link or a
hint.
"""

from __future__ import annotations

import os
from typing import Any

from rubisco.lib.l10n import _
from rubisco.lib.variable import format_str

__all__ = [
    "RUError",
    "RUOSError",
    "RUShellExecutionError",
    "RUValueError",
]


class RUError(RuntimeError):
    """Rubisco exception basic class."""

    docurl: str
    hint: str

    def __init__(
        self,
        *args: str | Exception,
        docurl: str = "",
        hint: str = "",
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Initialize a basic rubisco exception.

        Args:
            *args: Positional arguments.
            docurl (str, optional): Document link url. Defaults to "".
            hint (str, optional): Exception hint. Defaults to "".
            **kwargs: Keyword arguments.

        """
        self.docurl = docurl
        self.hint = hint
        super().__init__(*args, **kwargs)


class RUValueError(RUError, ValueError):
    """Rubisco value exception."""


class RUOSError(RUError, OSError):
    """OS Exception."""


class RUShellExecutionError(RUError):
    """Shell execution exception."""

    RETCODE_COMMAND_NOT_FOUND = 9009 if os.name == "nt" else 127

    retcode: int

    def __init__(
        self,
        *args: str,
        retcode: int = 0,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Initialize a shell execution exception.

        Args:
            *args: Positional arguments.
            retcode (int, optional): Shell return code. Defaults to 0.
            **kwargs: Keyword arguments.

        """
        hint = format_str(
            _("Subprocess return code is ${{retcode}}."),
            fmt={
                "retcode": str(retcode),
            },
        )
        if retcode == self.RETCODE_COMMAND_NOT_FOUND:
            hint = format_str(
                _(
                    "Subprocess return code is ${{retcode}}. "
                    "It may be caused by command not found.",
                ),
                fmt={"retcode": str(retcode)},
            )

        super().__init__(
            *args,
            docurl=str(kwargs.get("docurl", "")),
            hint=hint,
            **kwargs,
        )
        self.retcode = retcode
