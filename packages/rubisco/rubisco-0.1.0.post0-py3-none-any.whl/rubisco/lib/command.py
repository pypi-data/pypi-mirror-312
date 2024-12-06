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

"""Generate command line."""

from __future__ import annotations

__all__ = ["command"]


def command(args: list[str] | str) -> str:
    """Generate shell command from a list of arguments.

    Args:
        args (list[str] | str): The list of arguments.

    Returns:
        str: The shell command.

    """
    if isinstance(args, str):
        return args

    res_command = ""
    for arg in args:
        if " " in arg:
            if '"' in arg:
                arg = arg.replace('"', '\\"')  # noqa: PLW2901
            res_command += f'"{arg}" '
        else:
            res_command += f"{arg} "
    return res_command.strip()


if __name__ == "__main__":
    _CMD = command(["echo", "Hello, world!"])
    assert _CMD == 'echo "Hello, world!"'  # noqa: S101
    _CMD = command("echo Hello, world!")
    assert _CMD == "echo Hello, world!"  # noqa: S101
