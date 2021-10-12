"""
    sphinxnotes.recentupdate
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Sphinx extension for generating a list of recently updated documents from
    git log, outputted as both document and RSS .

    :copyright: Copyright 2021 Shengyu Zhang
    :license: BSD, see LICENSE for details.
"""

from __future__ import annotations
from typing import List, TYPE_CHECKING

from docutils.statemachine import StringList
from docutils.parsers.rst import directives

from sphinx.util.docutils import SphinxDirective
from sphinx.util import logging
if TYPE_CHECKING:
    from sphinx.application import Sphinx

__title__= 'sphinxnotes-recentupdate'
__license__ = 'BSD'
__version__ = '1.0a0'
__author__ = 'Shengyu Zhang'
__url__ = 'https://sphinx-notes.github.io/recentupdate'
__description__ = 'Sphinx extension for generating a list of recently updated documents from git log, outputted as both document and RSS'
__keywords__ = 'documentation, sphinx, extension, rss'

logger = logging.getLogger(__name__)

class RecentUpdateDirective(SphinxDirective):
    """
    """

    # Member of parent
    has_content:bool = True
    required_arguments:int = 1
    optional_arguments:int = 0
    final_argument_whitespace:bool = True
    option_spec:Dict[str,callable] = {}

    def run(self) -> List[nodes.Node]:
        return []


def setup(app:Sphinx) -> None:
    """Sphinx extension entrypoint."""
    app.add_directive('recentupdate', RecentUpdateDirective)
