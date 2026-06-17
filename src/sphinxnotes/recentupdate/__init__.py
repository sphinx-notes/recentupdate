"""
sphinxnotes.recentupdate
~~~~~~~~~~~~~~~~~~~~~~~~

Get recent document revision info from git, exposed as render extra context.

:copyright: Copyright 2021 Shengyu Zhang
:license: BSD, see LICENSE for details.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, ClassVar, override
from datetime import datetime, timezone
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


def get_git_revisions(
    repo: Repo,
    env: BuildEnvironment,
    count: int,
    path: str,
    current_doc: str | None = None,
) -> list[Revision]:
    revs: list[Revision] = []

    for cur in repo.iter_commits(paths=path):
        matches = [x in cur.message for x in env.config.recentupdate_exclude_commit]
        if any(matches):
            logger.debug(
                f'Skip commit {cur.hexsha}: excluded by recentupdate_exclude_commit'
            )
            continue

        prev = cur.parents[0] if len(cur.parents) != 0 else None

        m, a, d = [], [], []
        if prev is None:
            # Special case: root commit, all files are added
            for blob in cur.tree.traverse():
                if blob.type != 'blob':
                    continue
                docname = path2docname(repo, env, blob.path)
                if docname is None:
                    continue
                a.append(docname)
        else:
            diff_idx = prev.tree.diff(cur)
            for diff in diff_idx:
                if diff.a_path is None:
                    continue
                docname = path2docname(repo, env, diff.a_path)
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
            continue
        if current_doc is not None and current_doc not in (m + a + d):
            logger.debug(f'Skip commit {cur.hexsha}: no changes to {current_doc}')
            continue

        revs.append(
            Revision(
                message=str(cur.message).splitlines(),
                author=str(cur.author or ''),
                date=datetime.fromtimestamp(cur.authored_date, tz=timezone.utc),
                changed_docs=m,
                added_docs=a,
                removed_docs=d,
            )
        )
        if len(revs) >= count:
            break

    logger.info(
        f'[recentupdate] Intend to get recent {count} commits, eventually get {len(revs)}'
    )
    return revs


def path2docname(repo: Repo, env: BuildEnvironment, file: str) -> str | None:
    """Convert a repo-relative file path to a Sphinx docname."""
    relsrcdir_to_repo = path.relpath(env.srcdir, repo.working_dir)
    relfn_to_srcdir = path.relpath(file, relsrcdir_to_repo)
    absfn = Path(repo.working_dir, file)
    if not absfn.is_relative_to(env.srcdir):
        logger.debug(f'Skip {file}: out of srcdir')
        return None

    excluded = Matcher(env.config.exclude_patterns)
    if excluded(relfn_to_srcdir):
        logger.debug(f'Skip {file}: excluded by exclude_patterns')
        return None

    docname, ext = path.splitext(relfn_to_srcdir)
    source_suffix = list(env.config.source_suffix.keys())
    if not ext or ext not in source_suffix:
        logger.debug(f'Skip {file}: not {source_suffix} files')
        return None

    logger.debug(f'Get docname: {docname}')
    return docname


@extra_context('recentupdate')
class RecentUpdateExtraContext(ExtraContext):
    """Extra context providing recent document revisions from Git."""

    repo: ClassVar[Repo]

    @override
    def generate(
        self,
        req: ExtraContextRequest,
        count: int = 0,
        path: str = '.',
        current_doc: bool = False,
    ) -> Any:
        if count <= 0:
            count = req.env.config.recentupdate_count
        docname = req.env.docname if current_doc else None
        return get_git_revisions(self.repo, req.env, count, path, docname)


def setup(app: Sphinx):
    meta.pre_setup(app)

    RecentUpdateExtraContext.repo = Repo(app.srcdir, search_parent_directories=True)

    app.setup_extension('sphinxnotes.render')

    app.add_config_value(
        'recentupdate_exclude_commit', ['skip-recentupdate'], 'env', types=list[str]
    )

    app.add_config_value('recentupdate_count', 10, 'env', types=int)

    return meta.post_setup(app)
