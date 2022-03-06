"""
sphinxnotes.recentupdate
~~~~~~~~~~~~~~~~~~~~~~~~

Get the document update information from git and display it in Sphinx documentation.

:copyright: Copyright 2021 Shengyu Zhang
:license: BSD, see LICENSE for details.
"""

from __future__ import annotations
from typing import List, Iterable, TYPE_CHECKING, Optional
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
from sphinx.util.matching import Matcher
from sphinx.transforms import SphinxTransform
if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.config import Config
    from sphinx.environment import BuildEnvironment

from git import Repo
import jinja2

__title__= 'sphinxnotes-recentupdate'
__license__ = 'BSD'
__version__ = '1.0b1'
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

    def _get_docname(self, relfn_to_repo: str) -> Optional[str]:
        relsrcdir_to_repo = path.relpath(self.env.srcdir, self.repo.working_dir)
        relfn_to_srcdir = path.relpath(relfn_to_repo, relsrcdir_to_repo)
        absfn = path.abspath(relfn_to_srcdir)
        if path.commonpath([self.env.srcdir, absfn]) != self.env.srcdir:
            logger.debug(f'Skip {relfn_to_repo}: out of srcdir')
            return None

        excluded = Matcher(self.config.exclude_patterns)
        if excluded(relfn_to_srcdir):
            logger.debug(f'Skip {relfn_to_repo}: excluded by exclude_patterns confval')
            return None

        docname, ext = path.splitext(relfn_to_srcdir)
        source_suffix = list(self.config.source_suffix.keys())
        if not ext or ext not in source_suffix:
            logger.debug(f'Skip {relfn_to_repo}: not {source_suffix} files')
            return None

        for p in self.config.recentupdate_exclude_path:
            absp = path.abspath(p)
            if path.commonpath([absp, absfn]) == absp:
                logger.debug(f'Skip {relfn_to_repo}: excluded by recentupdate_exclude_path confval')
                return None

        logger.debug(f'Get docname: {docname}')
        return docname


    def _context(self, count: int) -> Dict[str,Any]:
        revisions = []
        res = { 'revisions': revisions }

        cur = self.repo.head.commit
        if cur is None:
            return res

        # Get recent N commits which contain document changes (N = count)
        n = 0
        while n < count:
            prev = cur.parents[0] if len(cur.parents) != 0 else None
            if prev is None:
                break

            m = []
            a = []
            d = []
            diff_idx = prev.tree.diff(cur)
            for diff in diff_idx:
                docname = self._get_docname(diff.a_path)
                if docname is None:
                    # Skip files out of srcdir
                    continue

                if diff.change_type == 'M':
                    m.append(docname)
                elif diff.change_type == 'A':
                    a.append(docname)
                elif diff.change_type == 'D':
                    d.append(docname)
                else:
                    logger.debug(f'Skip {diff.a_path}: unsupport change type {diff.change_type}')

            if len(m) + len(a) + len(d) == 0:
                # Dont create revisions when no document changes
                logger.debug(f'Skip commit {cur.hexsha}: no document changes')
                cur = prev
                continue

            revisions.append(Revision(message=cur.message,
                                      author=cur.author,
                                      date=datetime.utcfromtimestamp(cur.authored_date),
                                      modification=m,
                                      addition=a,
                                      deletion=d))
            cur = prev
            n += 1

        logger.debug(f'Intend to get recent {count} commits, eventually get {n}')

        return res


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
            msg = f'failed to render recentupdate template: {e}'
            logger.warning(msg, location=self.state.parent)
            sm = nodes.system_message(msg, type='WARNING', level=2, backrefs=[], source='')
            return [sm]
        else:
            nested_parse_with_titles(self.state, StringList(lines), self.state.parent)
            return []


DEFAULT_TEMPLATE = dedent('''
                          {% for r in revisions %}
                          {{ r.date | strftime }}
                            :Author: {{ r.author }}
                            :Message: {{ r.message }}

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

def setup(app:Sphinx):
    """Sphinx extension entrypoint."""

    # Set current git repo
    RecentUpdateDirective.repo = Repo(app.srcdir, search_parent_directories=True)

    app.add_directive('recentupdate', RecentUpdateDirective)

    app.add_config_value('recentupdate_count', 10, 'env')
    app.add_config_value('recentupdate_template', DEFAULT_TEMPLATE, 'env')
    app.add_config_value('recentupdate_date_format', '%Y-%m-%d', 'env')
    app.add_config_value('recentupdate_exclude_path', [], 'env')

    return {'version': __version__}
