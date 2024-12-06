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

"""Rubisco process control."""

from __future__ import annotations

import os
import sys
from subprocess import PIPE, STDOUT, Popen

import psutil

from rubisco.config import DEFAULT_CHARSET
from rubisco.lib.command import command
from rubisco.lib.exceptions import RUShellExecutionError
from rubisco.lib.fileutil import TemporaryObject
from rubisco.lib.l10n import _
from rubisco.lib.log import logger
from rubisco.lib.pathlib import Path
from rubisco.shared.ktrigger import IKernelTrigger, call_ktrigger

__all__ = ["Process", "is_valid_pid"]


def get_system_shell() -> str:
    """Get the system shell.

    Returns:
        str: The system shell.

    """
    if os.name == "nt":
        return os.environ.get("COMSPEC", "cmd.exe")
    return os.environ.get("SHELL", "/bin/sh")


class Process:
    """Process controler.

    Process's stdin/stdout/stderr will be direct to
    parent process's stdin/stdout/stderr. We will allocate a new console for
    non-console application on Windows.
    """

    origin_cmd: str  # For UCI's output.
    cmd: str
    cwd: Path
    process: Popen
    _tempfile: TemporaryObject | None

    def __init__(
        self,
        cmd: list[str] | str,
        cwd: Path | None = None,
    ) -> None:
        """Prepare to run a process."""
        if cwd is None:
            cwd = Path.cwd()

        if isinstance(cmd, str) and "\n" in cmd:
            self._tempfile = TemporaryObject.new_file(suffix=".bat")
            self._tempfile.path.write_text(
                f"{cmd}\n",
                encoding=DEFAULT_CHARSET,
            )
            self._tempfile.path.chmod(0o755)
            self.cmd = command([get_system_shell(), str(self._tempfile.path)])
        else:
            self.cmd = command(cmd)
            self._tempfile = None
        self.origin_cmd = command(cmd)
        self.cwd = cwd

    def run(
        self,
        fail_on_error: bool = True,  # noqa: FBT001 FBT002
    ) -> int:
        """Run the process.

        Args:
            fail_on_error (bool): Raise exception on error.

        Returns:
            int: The return code.

        """
        logger.debug(
            "Executing: %s cwd=%s\n%s",
            repr(self.cmd),
            self.cwd,
            self.origin_cmd,
        )
        call_ktrigger(IKernelTrigger.pre_exec_process, proc=self)
        with Popen(  # noqa: S602
            self.cmd,  # The executed command should be output.
            shell=True,  # We are not responsible for security.
            cwd=str(self.cwd),
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
        ) as self.process:
            ret = self.process.wait()
            raise_exc = ret != 0 and fail_on_error
            call_ktrigger(
                IKernelTrigger.post_exec_process,
                proc=self,
                retcode=ret,
                raise_exc=raise_exc,
            )
            if raise_exc:
                raise RUShellExecutionError(
                    _("Shell execution error."),  # type: ignore[arg-type]
                    retcode=ret,
                )

            return ret

    def popen(
        self,
        stdout: bool = True,  # noqa: FBT001 FBT002
        stderr: int = 1,
        fail_on_error: bool = True,  # noqa: FBT001 FBT002
        show_step: bool = True,  # noqa: FBT001 FBT002
    ) -> tuple[str, str, int]:
        """Run the command and return the stdout and stderr.

        Args:
            stdout (bool, optional): Return stdout. Defaults to True.
            stderr (int, optional): Return stderr. If 0, stderr will output.
                If 1, stderr will be returned. If 2, stderr will be redirected
                to stdout. Defaults to 1.
            fail_on_error (bool, optional): Raise an exception if return
                code != 0. Defaults to True.
            show_step (bool, optional): Call the pre_exec_process and
                post_exec_process triggers. Defaults to True.

        Returns:
            tuple[str, str]: The stdout and stderr. If stdout or stderr is not
                required, it will be "".

        Raises:
            RUShellExecutionError: If retcode !=0 and strict == True.

        """
        if show_step:
            call_ktrigger(IKernelTrigger.pre_exec_process, proc=self)
        with Popen(  # noqa: S602
            self.cmd,
            shell=True,
            cwd=str(self.cwd),
            stdin=sys.stdin,
            stdout=PIPE if stdout else sys.stdout,
            stderr=(
                PIPE
                if stderr == 1
                else (STDOUT if stderr == 2 else sys.stderr)  # noqa: PLR2004
            ),
        ) as self.process:
            ret = self.process.wait()
            raise_exc = ret != 0 and fail_on_error
            if show_step:
                call_ktrigger(
                    IKernelTrigger.post_exec_process,
                    proc=self,
                    retcode=ret,
                    raise_exc=raise_exc,
                )
            if raise_exc:
                raise RUShellExecutionError(
                    _("Shell execution error."),  # type: ignore[arg-type]
                    retcode=ret,
                )
            if stdout and self.process.stdout:
                stdout_data = self.process.stdout.read()
                stdout_data = stdout_data.decode(DEFAULT_CHARSET)
            else:
                stdout_data = ""
            if stderr == 1 and self.process.stderr:
                stderr_data = self.process.stderr.read()
                stderr_data = stderr_data.decode(DEFAULT_CHARSET)
            else:
                stderr_data = ""
            return stdout_data, stderr_data, ret

    def terminate(self) -> None:
        """Terminate the process."""
        self.process.terminate()
        self.process.wait()

    def __repr__(self) -> str:
        """Return the string representation of the object.

        Returns:
            str: The string representation.

        """
        if self._tempfile:
            return f"Process({self.origin_cmd!r})"
        return f"Process({self.cmd!r})"


def is_valid_pid(pid: int) -> bool:
    """Check if a pid is valid.

    Args:
        pid (int): The pid to check.

    Returns:
        bool: True if the pid is valid, otherwise False.

    """
    return psutil.pid_exists(pid)


if __name__ == "__main__":
    import pytest

    # Test: Process.
    p = Process("echo Hello, world!")
    p.run()
    p = Process(["echo", "Hello, world!"])
    p.run()

    # Test: Process with error
    p = Process("echo Hello, world! && exit 1")
    pytest.raises(RUShellExecutionError, lambda: p.run(fail_on_error=True))

    # Test: Process with error.
    p = Process("echo Hello, world! && exit 1")
    p.run(fail_on_error=False)

    # Test: Popen.
    stdout_, stderr_, retcode_ = Process("echo Hello, world!").popen()
    assert stdout_ == "Hello, world!\n"  # noqa: S101
    assert stderr_ == ""  # noqa: S101
    assert retcode_ == 0  # noqa: S101

    # Test: Popen with an exception.
    pytest.raises(
        RUShellExecutionError,
        lambda: Process(
            "false",
        ).popen(stdout=False, stderr=1),
    )

    # Test: A multiline command.
    p = Process("echo line1 \n echo line2")
    assert p.run() == 0  # noqa: S101

    # Test: A multiline popen.
    stdout_, stderr_, retcode_ = Process("echo line1 \n echo line2").popen()
    assert stdout_.strip() == "line1\nline2"  # noqa: S101
    assert stderr_ == ""  # noqa: S101
    assert retcode_ == 0  # noqa: S101

    # Test: Popen with stderr redirection.
    stdout_, stderr_, retcode_ = Process("echo Hello, world! >&2").popen(
        stderr=2,
    )
    assert stdout_ == "Hello, world!\n"  # noqa: S101
    assert stderr_ == ""  # noqa: S101
    assert retcode_ == 0  # noqa: S101

    # Test: PID check.
    assert is_valid_pid(0)  # noqa: S101
