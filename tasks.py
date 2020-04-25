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
FLAKE8 = which('flake8') if which('flake8') else (VENV / Path('bin') / 'flake8')
ISORT = which('isort') if which('isort') else (VENV / Path('bin') / 'isort')
PYTEST = which('pytest') if which('pytest') else (VENV / Path('bin') / 'pytest')
PIP = which('pip') if which('pip') else (VENV / Path('bin') / 'pip')
POETRY = which('poetry') if which('poetry') else (VENV / Path('bin') / 'poetry')
PRECOMMIT = which('pre-commit') if which('pre-commit') else (VENV / Path('bin') / 'pre-commit')


@task
def tests(c):
    """Run the test suite"""
    c.run(f'{PYTEST}', pty=True)


@task
def isort(c, check=False):
    check_flag = ''
    if check:
        check_flag = '-c'
    c.run(f'{ISORT} {check_flag} --recursive {PKG_PATH}/* tasks.py')


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
