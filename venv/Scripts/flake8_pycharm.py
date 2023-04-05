#!C:\Users\Vladislav\Desktop\dev_pr\dont_try_this_at_home\venv\Scripts\python.exe
"""This command tries to emulate pylint in order to get pycharm work using flake8."""
import argparse
import contextlib
import getpass
import json
import os
import shutil
import signal
import subprocess  # noqa: S404
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(sys.argv[0])

PID_FILE = "{temp_dir}/{user}_flake8_pid".format(
    temp_dir=tempfile.gettempdir(),
    user=getpass.getuser(),
)

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--output-format")
parser.add_argument("--help-msg")
parser.add_argument("--rcfile")
parser.add_argument("--with-pylint", action="store_true")
parser.add_argument("files", nargs="*")

args = parser.parse_args()
flake8_args = ["flake8", "--format=pycharm"]


def ensure_only_one_flake8_instance_is_running():
    """
    Ensure that only one instance of this program is running.

    If another instance is found, it will be terminated.
    """
    if os.path.isfile(PID_FILE):
        with open(PID_FILE) as pid_file:
            old_pid = pid_file.read().strip()
            with contextlib.suppress(ProcessLookupError):
                os.kill(int(old_pid), signal.SIGTERM)
    pid = os.getpid()
    with open(PID_FILE, "w") as new_pid_file:
        new_pid_file.write(str(pid))


def get_json_from_linter(linter_args: list) -> list:
    """Will Run flake8 or Pylint and return their output in json format."""
    linter_args[0] = shutil.which(linter_args[0], path=SCRIPT_DIR)
    pipe = subprocess.Popen(  # noqa: S603
        linter_args,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
    )
    try:
        return json.loads(pipe.communicate()[0])
    except json.JSONDecodeError:
        print("{linter} command failed".format(linter=linter_args[0]))  # noqa: 421
        sys.exit(1)


if args.help_msg:
    print(  # noqa: WPS421
        ":no-member (E1101): *%s %r has no %r member%s*\n"  # noqa: WPS323
        "  Used when a variable is accessed for an unexistent member. This message\n"
        "  belongs to the typecheck checker.\n"
    )
    sys.exit(0)

if args.output_format != "json":
    # Attempting to call pylint?
    os.execlp("pylint", *sys.argv)  # noqa:S607,S606

if args.rcfile:
    flake8_args.append("--config")
    flake8_args.append(args.rcfile)

flake8_args += args.files

ensure_only_one_flake8_instance_is_running()
flake8_output = get_json_from_linter(flake8_args)

if args.with_pylint:
    pylint_args = ["pylint", "-f", "json"]
    if args.rcfile:
        pylint_args += ["--rcfile", args.rcfile]
    pylint_args += args.files
    flake8_output += get_json_from_linter(pylint_args)

print(json.dumps(flake8_output, indent=4))  # noqa: WPS421
