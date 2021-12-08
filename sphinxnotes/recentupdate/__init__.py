"""
sphinxnotes.recentupdate
~~~~~~~~~~~~~~~~~~~~~~~~

Get the document update information from git and display it in Sphinx documentation.

:copyright: Copyright 2021 Shengyu Zhang
:license: BSD, see LICENSE for details.
"""

from __future__ import annotations
from typing import List, Iterable, TYPE_CHECKING
from textwrap import dedent
from datetime import datetime
from enum import Enum, auto
from dataclasses import dataclass
from os import path

from docutils import nodes
from docutils.statemachine import StringList
from docutils.parsers.rst import directives, Parser
from docutils.utils import new_document

from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.transforms import SphinxTransform
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.environment import BuildEnvironment

from git import Repo
import jinja2

__title__= 'sphinxnotes-recentupdate'
__license__ = 'BSD'
__version__ = '1.0a1'
__author__ = 'Shengyu Zhang'
__url__ = 'https://sphinx-notes.github.io/recentupdate'
__description__ = 'Get document change information from git log and Display in Sphinx documentation'
__keywords__ = 'documentation, sphinx, extension, rss, git'

logger = logging.getLogger(__name__)


class Environment(jinja2.Environment):
    datefmt:str

    def __init__(self, datefmt:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.datefmt = datefmt
        self.filters['strftime'] = self._strftime_filter
        self.filters['roles'] = self._roles_filter

    def _strftime_filter(self, value, format=None) -> str:
        """
        Filter for stringify datetime given format.
        if no format given, use confval "recentupdate_date_format".
        """
        if format is None:
            format = self.datefmt
        return value.strftime(format)

    def _roles_filter(self, value:Iterable[str], role:str) -> Iterable[str]:
        """
        A heplfer filter for converting list of string to list of role.

        For example::

            {{ ["foo", "bar"] | roles("doc") }}

        Produces ``[":doc:`foo`", ":doc:`bar`"]``.
        """
        return map(lambda x: ':%s:`%s`' % (role, x), value)


@dataclass
class Revision(object):
    """
    Revision represents a git commit which contains document changes.
    """

    #: Git commit message
    message:str
    #: Git commit author
    author:str
    #: Git commit author date
    date:datetime

    # FYI, possible status letters are:
    # :A: addition of a file
    # :C: copy of a file into a new one
    # :D: deletion of a file
    # :M: modification of the contents or mode of a file
    # :R: renaming of a file
    # :T: change in the type of the file
    # :U: file is unmerged (you must complete the merge before it can be committed)
    # :X: "unknown" change type (most probably a bug, please report it)

    #: List of docname, corresponding to files which are modified
    addition:List[str]
    #: List of docname, corresponding to files which are newly added
    modification:List[str]
    #: List of docname, corresponding to files which are deleted
    deletion:List[str]


class RecentUpdateDirective(SphinxDirective):
    """ Directive for displaying recent update.  """

    # Member of parent
    has_content:bool = True
    required_arguments:int = 0
    optional_arguments:int = 1
    final_argument_whitespace:bool = False
    option_spec = {}

    #: Repo info
    repo:Repo = None

    @staticmethod
    def _in_srcdir(rel_srcdir: str, rel_fn: str) -> bool:
        srcdir = path.abspath(rel_srcdir)
        fn = path.abspath(rel_fn)
        return path.commonpath([srcdir, fn]) == srcdir


    def _context(self, count: int) -> Dict[str,Any]:
        assert(self.repo.head)

        logger.debug("Intend to get recent %s commits", count)
        # Get recent N commits (N = count)
        ptr = self.repo.head.commit
        commits = []
        for i in range(0, count+1):
            if ptr is None:
                break
            commits.append(ptr)
            ptr = ptr.parents[0] if len(ptr.parents) != 0 else None
        logger.debug("Get recent %s commits eventually", len(commits))

        revisions = []
        rel_srcdir = path.relpath(self.env.srcdir, self.repo.working_dir) # Relative sphinx doc source dir
        logger.debug("Relative srcdir: %s", rel_srcdir)

        for i in range(1, len(commits)):
            m = []
            a = []
            d = []
            diff_idx = commits[i].tree.diff(commits[i-1])
            for diff in diff_idx:
                if not self._in_srcdir(rel_srcdir, diff.a_path):
                    # Skip files out of srcdir
                    logger.debug("Skip %s: out of srcdir", diff.a_path)
                    continue
                rel_a_path = path.relpath(diff.a_path, rel_srcdir)
                docname, ext = path.splitext(rel_a_path)
                source_suffix = list(self.config.source_suffix.keys())
                if ext not in source_suffix:
                    # Skip non-source files
                    logger.debug("Skip %s: not %s files", diff.a_path, source_suffix)
                    continue

                logger.debug("doc %s, change_type %s", diff.a_path, diff.change_type)
                if diff.change_type == 'M':
                    m.append(docname)
                elif diff.change_type == 'A':
                    a.append(docname)
                elif diff.change_type == 'D':
                    d.append(docname)
                else:
                    logger.debug("Skip %s: unsupport change type %s", diff.a_path, diff.change_type)

            if len(m) + len(a) + len(d) == 0:
                # Dont create revisions when no document changes
                logger.debug("Skip commit %s: no document changes", commits[i].hexsha)
                continue

            revisions.append(Revision(message=commits[i].message,
                                      author=commits[i].author,
                                      date=datetime.utcfromtimestamp(commits[i-1].authored_date),
                                      modification=m,
                                      addition=a,
                                      deletion=d))
        return { 'revisions': revisions }


    def run(self) -> List[nodes.Node]:
        if len(self.arguments) >= 1:
            count = directives.nonnegative_int(self.arguments[0])
        else:
            count = self.config.recentupdate_count

        # Render reST from Jinja template, then parse it in to document
        env = Environment(self.config.recentupdate_date_format)

        try:
            template = env.from_string('\n'.join(list(self.content)) or self.config.recentupdate_template)
            lines = template.render(self._context(count)).split('\n')
        except Exception as e:
            msg = "failed to render recentupdate template: %s" % e
            logger.warning(msg, location=self.state.parent)
            sm = nodes.system_message(msg, type='WARNING', level=2, backrefs=[], source='')
            return [sm]
        else:
            nested_parse_with_titles(self.state, StringList(lines), self.state.parent)
            return []


DEFAULT_TEMPLATE = dedent('''
                          {% for r in revisions %}
                          :On {{ r.date | strftime }}, {{ r.author }}:
                             {% if r.modification %}
                             - Modified {{ r.modification | roles("doc") | join(", ") }}
                             {% endif %}
                             {% if r.addition %}
                             - Added {{ r.addition | roles("doc") | join(", ") }}
                             {% endif %}
                             {% if r.deletion %}
                             - Deleted {{ r.deletion | join(", ") }}
                             {% endif %}
                          {% endfor %}
                          ''')

def setup(app:Sphinx) -> None:
    """Sphinx extension entrypoint."""

    # Set current git repo
    RecentUpdateDirective.repo = Repo(app.srcdir, search_parent_directories=True)

    app.add_directive('recentupdate', RecentUpdateDirective)

    app.add_config_value('recentupdate_count', 10, 'env')
    app.add_config_value('recentupdate_template', DEFAULT_TEMPLATE, 'env')
    app.add_config_value('recentupdate_date_format', '%Y-%m-%d', 'env')

