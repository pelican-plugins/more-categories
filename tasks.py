import os
from pathlib import Path
from shutil import which

from invoke import task

PKG_NAME = 'more_categories'
PKG_PATH = Path(f'pelican/plugins/{PKG_NAME}')

ACTIVE_VENV = os.environ.get("VIRTUAL_ENV", None)
VENV_HOME = Path(os.environ.get("WORKON_HOME", "~/.local/share/virtualenvs"))
VENV_PATH = Path(ACTIVE_VENV) if ACTIVE_VENV else (VENV_HOME / PKG_NAME)
VENV = str(VENV_PATH.expanduser())


TOOLS = ['poetry', 'pre-commit']
FLAKE8 = which('flake8') or Path(f'{VENV}/bin/flake8')
ISORT = which('isort') or Path(f'{VENV}/bin/isort')
PYTEST = which('pytest') or Path(f'{VENV}/bin/pytest')
PIP = which('pip') or Path(f'{VENV}/bin/pip')
POETRY = which('poetry') or Path(f'{VENV}/bin/poetry')
PRECOMMIT = which('pre-commit') or Path(f'{VENV}/bin/pre-commit')


@task
def tests(c):
    """Run the test suite"""
    c.run(f'{PYTEST}', pty=True)


@task
def isort(c, check=False, diff=False):
    check_flag, diff_flag = '', ''
    if check:
        check_flag = '-c'
    if diff:
        diff_flag = '--diff'
    c.run(f'{ISORT} {check_flag} {diff_flag} --recursive {PKG_PATH}/* tasks.py')


@task
def flake8(c):
    c.run(f'{FLAKE8} {PKG_PATH} tasks.py')


@task
def lint(c):
    isort(c, check=True)
    flake8(c)


@task
def tools(c):
    """Install tools in the virtual environment if not already on PATH"""
    for tool in TOOLS:
        if not which(tool):
            c.run(f'{PIP} install {tool}')


@task
def precommit(c):
    """Install pre-commit hooks to .git/hooks/pre-commit"""
    c.run(f'{PRECOMMIT} install')


@task
def setup(c):
    c.run(f'{PIP} install -U pip')
    tools(c)
    c.run(f'{POETRY} install')
    precommit(c)
