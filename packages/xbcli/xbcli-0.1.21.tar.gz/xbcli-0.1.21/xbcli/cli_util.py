# -*- encoding: utf-8 -*-
import contextlib
import os
import platform
import random
import re
import shutil
import string
import subprocess
import sys
import typing as t

import click
import psutil
from click import testing
from flask import Flask

__all__ = [
    "app_cli_runner",
    "check_output",
    "click_echo",
    "click_exit",
    "conda_command",
    "conda_executable",
    "init_conda",
    "new_conda_env",
    "platform_uname",
    "random_string",
    "run_command",
    "run_subprocess",
    "sample_string",
]


def sample_string(source: str, num: int) -> str:
    return "".join([random.choice(source) for _ in range(num)])


def random_string(num: int = 8) -> str:
    first_char = sample_string(string.ascii_letters, 1)
    return first_char + sample_string(string.ascii_letters + string.digits, num - 1)


def platform_uname(conda_env: str) -> str:
    script = "\"import sys; print(f'{sys.version_info.major}{sys.version_info.minor}');\""
    result = check_output(conda_executable("python", "-c", script, conda_env=conda_env), echo=False)
    assert len(result) >= 1

    if sys.platform == "win32":
        return f"cp{result[0]}-win_{platform.machine().lower()}"
    elif sys.platform == "linux":
        return f"cpython-{result[0]}-{platform.machine().lower()}-linux"
    elif sys.platform == "darwin":
        return f"cpython-{result[0]}-darwin"
    else:
        raise Exception(f"platform not support: {platform.uname()}")


def click_echo(message: str, err: bool = False, fg: str | None = None):
    if err is True:
        click.echo(click.style(message, fg=fg or "red"))
    else:
        click.echo(click.style(message, fg=fg))


def click_exit(message: str, return_code: int = 1):
    click_echo(message, err=True)
    sys.exit(return_code)


def app_cli_runner(app: Flask, *args: str):
    with app.app_context():
        runner = app.test_cli_runner()
        result: testing.Result = runner.invoke(args=args)
        if result.stdout_bytes:
            print(result.stdout_bytes.decode("utf-8"))
        if result.stderr_bytes:
            print(result.stderr_bytes.decode("utf-8"))


def run_command(*args: str, echo: bool = True, executable: str | None = None) -> int:
    if executable is None:
        command = " ".join(args)
    else:
        command = f'{executable} {" ".join(args)}'

    if echo is True:
        print(">>>", command)
    return os.system(command)


def run_subprocess(
    *args: str,
    echo: bool = True,
    shell: bool = True,
    executable: str | None = None,
    detached: bool = False,
    priority: int | None = None,
) -> int:
    if echo is True:
        if executable is None:
            print(">>>", *args)
        else:
            print(">>>", executable, *args)

    kwargs: dict[str, t.Any] = dict()
    if sys.platform.startswith("win32"):
        kwargs.update(
            startupinfo=subprocess.STARTUPINFO(
                dwFlags=subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW,
                wShowWindow=subprocess.SW_HIDE,
            )
        )
        if detached is True:
            kwargs.update(creationflags=subprocess.DETACHED_PROCESS)
        else:
            kwargs.update(creationflags=subprocess.HIGH_PRIORITY_CLASS)
    else:
        raise Exception(f"platform not support: {sys.platform}")

    kwargs.update(
        shell=shell,
        executable=executable,
    )
    if detached is True:
        kwargs.update(
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        p = subprocess.Popen(" ".join(args), **kwargs)
        if priority is not None:
            psutil.Process(p.pid).nice(priority)
        return 0
    else:
        kwargs.update(
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        p = subprocess.Popen(" ".join(args), **kwargs)
        if priority is not None:
            psutil.Process(p.pid).nice(priority)
        while True:
            if p.stdout is None:
                break

            output = p.stdout.readline()
            if not output and p.poll() is not None:
                break

            if isinstance(output, bytes):
                if len(output):
                    print(output.decode("gbk"), end="")
            else:
                if len(output):
                    print(output, end="")

        while True:
            if p.stderr is None:
                break

            output = p.stderr.readline()
            if not output and p.poll() is not None:
                break

            if isinstance(output, bytes):
                if len(output):
                    print(output.decode("gbk"), end="")
            else:
                if len(output):
                    print(output, end="")

        return p.poll() or 0


def check_output(
    *args: str,
    cwd: str | None = None,
    executable: str | None = None,
    encoding: str = "utf-8",
    echo: bool = True,
    shell: bool = True,
) -> list[str]:
    if cwd is None:
        cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    previous_cwd = os.getcwd()
    os.chdir(cwd)
    if echo is True:
        print(">>>", " ".join(args).replace("\r\n", "\\n").replace("\n", "\\n"))
    result = subprocess.check_output(" ".join(args), executable=executable, shell=shell)
    os.chdir(previous_cwd)
    if isinstance(result, (bytes, bytearray)):  # type: ignore
        text = result.decode(encoding)
    elif isinstance(result, memoryview):  # type: ignore
        text = result.tobytes().decode(encoding)
    else:
        text = result

    if echo is True:
        print(text)
    return re.split("\r?\n", text)


def conda_executable(*args: str, conda_env: str) -> str:
    if len(args) == 0:
        raise Exception("command_args not specified")

    if sys.platform.startswith("win32"):
        result = check_output("where conda", echo=False)
    else:
        result = check_output("which conda", echo=False)

    if len(result) == 0 or len(result[0]) == 0:
        click_exit("conda not found")

    conda_filename = result[0]

    result = check_output(f"{conda_filename} env list", echo=False)
    if not any((text.startswith(conda_env + " ") for text in result)):
        click_exit(f"entry_python not found: {conda_env}")

    if sys.platform.startswith("win32"):
        if re.match("^(python[3]?$|python[3]? )", args[0]):
            return os.path.abspath(os.path.join(os.path.dirname(conda_filename), f"../envs/{conda_env}")) + os.sep + " ".join(args)
        else:
            return os.path.abspath(os.path.join(os.path.dirname(conda_filename), f"../envs/{conda_env}/Scripts")) + os.sep + " ".join(args)
    else:
        return os.path.abspath(os.path.join(os.path.dirname(conda_filename), f"../envs/{conda_env}/bin")) + os.sep + " ".join(args)


def conda_command(
    *args: str,
    conda_env: str,
    shell: bool = True,
    echo: bool = True,
    detached: bool = False,
    priority: int | None = None,
) -> int:
    if echo is True:
        print(">>>", " ".join(args))

    command = conda_executable(*args, conda_env=conda_env)

    if detached is True:
        return run_subprocess(command, shell=shell, detached=True, priority=priority)

    if priority is not None:
        return run_subprocess(command, shell=shell, priority=priority)
    else:
        return run_command(command, echo=False)


def init_conda(env_name: str, python_version: str, force: bool = False, requirements_txt: str | None = None) -> int:
    if sys.platform.startswith("win32"):
        result = check_output("where conda", echo=False)
    else:
        result = check_output("which conda", echo=False)

    if len(result) == 0 or len(result[0]) == 0:
        click_exit("conda not found")

    conda_filename = result[0]

    result = check_output(f"{conda_filename} env list")
    print(f"\n{env_name}")
    print("=" * 32)

    ret = -1
    if any((text.startswith(env_name + " ") for text in result)):
        if force is True:
            ret = run_command(f"{conda_filename} remove -n {env_name} --all -y")
            environment_path = os.path.abspath(os.path.join(os.path.dirname(conda_filename), f"../envs/{env_name}"))
            if os.path.isdir(environment_path):
                shutil.rmtree(environment_path)
            ret = run_command(f"{conda_filename} create -q --no-default-packages --name {env_name} python={python_version} -y")
    else:
        ret = run_command(f"{conda_filename} create -q --no-default-packages --name {env_name} python={python_version} -y")

    if requirements_txt is not None:
        ret = conda_command(f'pip install --no-warn-script-location -r "{requirements_txt}"', conda_env=env_name)

    return ret


@contextlib.contextmanager
def new_conda_env(random_tag: str, python_version: str, *, requirements_txt: str | None = None) -> t.Iterator[str]:
    if not bool(re.fullmatch("\\d+\\.\\d+", python_version)):
        raise ValueError("invalid python_version, {}".format(python_version))

    conda_env = "{}_{}".format(random_tag, python_version.replace(".", ""))
    run_command(f"conda create -n {conda_env} python={python_version} -y")
    if requirements_txt is not None:
        conda_command(f"pip install --no-warn-script-location -r {requirements_txt}", conda_env=conda_env)
    try:
        yield conda_env
    finally:
        run_command(f"conda remove -n {conda_env} --all -y")
