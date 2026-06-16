from pathlib import Path
import os
import sys
import pytest

pytest_plugins = 'sphinx.testing.fixtures'

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))


@pytest.fixture(scope='session')
def rootdir() -> Path:
    return Path(__file__).parent / 'roots'


@pytest.fixture(autouse=True)
def _restore_git(app_params):
    """Rename .gitdata -> .git before build, .git -> .gitdata after."""
    srcdir = app_params.kwargs['srcdir']
    gitdata = srcdir / '.gitdata'
    git = srcdir / '.git'

    if gitdata.exists():
        gitdata.rename(git)

    yield

    if git.exists():
        git.rename(gitdata)
