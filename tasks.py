from pathlib import Path

from invoke import task

PKG_NAME = 'more_categories'
PKG_PATH = Path(f'pelican/plugins/{PKG_NAME}')
FLAKE8 = 'flake8'
ISORT = 'isort'
PYTEST = 'pytest'


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
