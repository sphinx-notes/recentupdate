"""
sphinxnotes.recentupdate
~~~~~~~~~~~~~~~~~~~~~~~~

Get recent document revision info from git, exposed as render extra context.

:copyright: Copyright 2021 Shengyu Zhang
:license: BSD, see LICENSE for details.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, ClassVar
from datetime import datetime
from dataclasses import dataclass
from os import path
from pathlib import Path

from git import Repo

from sphinx.util import logging
from sphinx.util.matching import Matcher

from sphinxnotes.render import (
    extra_context,
    ExtraContext,
    ExtraContextRequest,
)

from . import meta

if TYPE_CHECKING:
    from typing import Any
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment

logger = logging.getLogger(__name__)


@dataclass
class Revision:
    #: Git commit message, split by lines
    message: list[str]
    #: Git commit author
    author: str
    #: Git commit author date
    date: datetime

    # FYI, possible status letters are:
    # :A: addition of a file
    # :C: copy of a file into a new one
    # :D: deletion of a file
    # :M: modification of the contents or mode of a file
    # :R: renaming of a file
    # :T: change in the type of the file
    # :U: file is unmerged (you must complete the merge before it can be committed)
    # :X: "unknown" change type (most probably a bug, please report it)

    #: List of docname, corresponding to files which are newly added
    added_docs: list[str]
    #: List of docname, corresponding to files which are modified
    changed_docs: list[str]
    #: List of docname, corresponding to files which are deleted
    removed_docs: list[str]


@extra_context('recentupdate')
class RecentUpdateExtraContext(ExtraContext):
    """Extra context providing recent document revisions from Git."""

    repo: ClassVar[Repo]

    def generate(self, req: ExtraContextRequest, *args, **kwargs) -> Any:
        count = args[0] if args else kwargs.get('count', 10)
        return self._revisions(req.env, count)

    def _get_docname(self, env: BuildEnvironment, file_path: str) -> str | None:
        """Convert a repo-relative file path to a Sphinx docname."""
        relsrcdir_to_repo = path.relpath(env.srcdir, self.repo.working_dir)
        relfn_to_srcdir = path.relpath(file_path, relsrcdir_to_repo)
        absfn = Path(self.repo.working_dir, file_path)
        if not absfn.is_relative_to(env.srcdir):
            logger.debug(f'Skip {file_path}: out of srcdir')
            return None

        excluded = Matcher(env.config.exclude_patterns)
        if excluded(relfn_to_srcdir):
            logger.debug(f'Skip {file_path}: excluded by exclude_patterns')
            return None

        docname, ext = path.splitext(relfn_to_srcdir)
        source_suffix = list(env.config.source_suffix.keys())
        if not ext or ext not in source_suffix:
            logger.debug(f'Skip {file_path}: not {source_suffix} files')
            return None

        for p in env.config.recentupdate_exclude_path:
            exclude_path = Path(env.srcdir, p)
            if absfn.is_relative_to(exclude_path):
                logger.debug(f'Skip {file_path}: excluded by path {exclude_path}')
                return None

        logger.debug(f'Get docname: {docname}')
        return docname

    def _revisions(self, env: BuildEnvironment, count: int) -> list[Revision]:
        revisions: list[Revision] = []

        cur = self.repo.head.commit
        if cur is None:
            return revisions

        n = 0
        while n < count:
            prev = cur.parents[0] if len(cur.parents) != 0 else None
            if prev is None:
                break

            matches = [x in cur.message for x in env.config.recentupdate_exclude_commit]
            if any(matches):
                logger.debug(
                    f'Skip commit {cur.hexsha}: excluded by recentupdate_exclude_commit'
                )
                cur = prev
                continue

            m, a, d = [], [], []
            diff_idx = prev.tree.diff(cur)
            for diff in diff_idx:
                if diff.a_path is None:
                    continue
                docname = self._get_docname(env, diff.a_path)
                if docname is None:
                    continue

                if diff.change_type == 'M':
                    m.append(docname)
                elif diff.change_type == 'A':
                    a.append(docname)
                elif diff.change_type == 'D':
                    d.append(docname)
                else:
                    logger.info(
                        f'Skip {diff.a_path}: '
                        f'unsupported change type {diff.change_type}'
                    )

            if len(m) + len(a) + len(d) == 0:
                logger.debug(f'Skip commit {cur.hexsha}: no document changes')
                cur = prev
                continue

            revisions.append(
                Revision(
                    message=cur.message.splitlines(),
                    author=str(cur.author or ''),
                    date=datetime.utcfromtimestamp(cur.authored_date),
                    changed_docs=m,
                    added_docs=a,
                    removed_docs=d,
                )
            )
            cur = prev
            n += 1

        logger.info(
            f'[recentupdate] Intend to get recent {count} commits, eventually get {n}'
        )

        return revisions


def setup(app: Sphinx):
    meta.pre_setup(app)

    RecentUpdateExtraContext.repo = Repo(app.srcdir, search_parent_directories=True)

    app.setup_extension('sphinxnotes.render')

    app.add_config_value('recentupdate_exclude_path', [], 'env', types=list[str])
    app.add_config_value(
        'recentupdate_exclude_commit', ['skip-recentupdate'], 'env', types=list[str]
    )

    return meta.post_setup(app)
