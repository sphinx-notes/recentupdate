"""
sphinxnotes.recentupdate
~~~~~~~~~~~~~~~~~~~~~~~~

Get recent document revision info from git, exposed as render extra context.

:copyright: Copyright 2021 Shengyu Zhang
:license: BSD, see LICENSE for details.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, ClassVar, Iterator, override
from datetime import datetime, timezone
from dataclasses import dataclass
from collections import OrderedDict
from os import path
from itertools import islice

from git import Repo

from sphinx.util import logging
from sphinx.config import ENUM

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

    #: List of docname, corresponding to files which are newly added
    added_docs: list[str]
    #: List of docname, corresponding to files which are modified
    changed_docs: list[str]
    #: List of docname, corresponding to files which are deleted
    removed_docs: list[str]


def get_time_period_key(dt: datetime, group_by: str) -> datetime:
    """Return the start of the time period for grouping."""
    if group_by == 'day':
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    elif group_by == 'month':
        return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif group_by == 'year':
        return dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    return dt


def compact_revision(revs: list[Revision]) -> Revision:
    if len(revs) == 1:
        return revs[0]

    messages = []
    for rev in reversed(revs):
        messages.extend(rev.message)

    added, changed, removed = set(), set(), set()
    for rev in reversed(revs):
        added.update(rev.added_docs)
        changed.update(rev.changed_docs)
        removed.update(rev.removed_docs)

    # Compute the net effect of all commits in this group:
    # If a file was added then deleted, the net effect is removal.
    # If a file was added then modified, the net effect is addition.
    # If a file was modified then deleted, the net effect is removal.
    # FIXME: If a files is removed and then re-added, ...
    added -= removed
    changed -= removed
    changed -= added

    return Revision(
        message=messages,
        author=revs[0].author,
        date=revs[0].date,
        added_docs=sorted(added),
        changed_docs=sorted(changed),
        removed_docs=sorted(removed),
    )


def group_revisions(
    groups: OrderedDict[tuple[str, datetime], list[Revision]],
    rev: Revision,
    group_by: str,
) -> None:
    """Add revision to groups."""
    key = (rev.author, get_time_period_key(rev.date, group_by))
    groups.setdefault(key, []).append(rev)


def compact_groups(
    groups: OrderedDict[tuple[str, datetime], list[Revision]],
) -> list[Revision]:
    """Compact grouped revisions into a list of Revision."""
    merged = []
    for (author, period_date), revs in groups.items():
        rev = compact_revision(revs)
        rev.author, rev.date = author, period_date
        merged.append(rev)
    return merged


def get_git_revisions(
    repo: Repo,
    env: BuildEnvironment,
    paths: list[str],
) -> Iterator[Revision]:
    """Yield Revision objects from git commits."""
    for cur in repo.iter_commits(paths=paths):
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
                docname = path2doc(repo, env, blob.path)
                if docname is None:
                    continue
                a.append(docname)
        else:
            # Possible status letters are:
            # :A: addition of a file
            # :C: copy of a file into a new one
            # :D: deletion of a file
            # :M: modification of the contents or mode of a file
            # :R: renaming of a file
            # :T: change in the type of the file
            # :U: file is unmerged (you must complete the merge before it can be committed)
            # :X: "unknown" change type (most probably a bug, please report it)
            status_maps = {'M': m, 'A': a, 'D': d }

            # Use git diff --name-status with pathspecs for native pathspec matching
            name_status = repo.git.diff(
                prev.hexsha, cur.hexsha, '--name-status', '--', *paths
            )
            for line in name_status.splitlines():
                if not line.strip():
                    continue
                status, file_path = line.split('\t', 1)
                docname = path2doc(repo, env, file_path)
                if docname is None:
                    continue

                if status in status_maps:
                    status_maps[status].append(docname)
                else:
                    logger.info(f'Skip {file_path}: unsupported change type {status}')

        if len(m) + len(a) + len(d) == 0:
            logger.debug(f'Skip commit {cur.hexsha}: no document changes')
            continue

        yield Revision(
            message=str(cur.message).splitlines(),
            author=str(cur.author or ''),
            date=datetime.fromtimestamp(cur.authored_date, tz=timezone.utc),
            changed_docs=m,
            added_docs=a,
            removed_docs=d,
        )


def path2doc(repo: Repo, env: BuildEnvironment, blob_path: str) -> str | None:
    """Convert a git repo-relative blob path to a Sphinx document name. """
    return env.path2doc(path.join(repo.working_dir, blob_path))


@extra_context('recentupdate')
class RecentUpdateExtraContext(ExtraContext):
    """Extra context providing recent document revisions from Git."""

    repo: ClassVar[Repo]

    @override
    def generate(
        self,
        req: ExtraContextRequest,
        count: int = 0,
        paths: list[str] = ['.', ],
        current_doc: bool = False,
        group_by: str = '',
    ) -> Any:
        count = count or req.env.config.recentupdate_count
        group_by = group_by or req.env.config.recentupdate_group_by

        if current_doc:
            docpath = req.env.doc2path(req.env.docname)
            repo_path = path.relpath(docpath, self.repo.working_dir)
            paths = [repo_path]

        git_revs = get_git_revisions(self.repo, req.env, paths)

        if group_by:
            groups = OrderedDict()
            for rev in git_revs:
                group_revisions(groups, rev, group_by)
                if len(groups) >= count:
                    break
            revs = compact_groups(groups)
        else:
            revs = list(islice(git_revs, count))
        logger.info(
            f'[recentupdate] Expect {count} revisions, finally get {len(revs)}, group by {group_by}'
        )

        return revs


def setup(app: Sphinx):
    meta.pre_setup(app)

    RecentUpdateExtraContext.repo = Repo(app.srcdir, search_parent_directories=True)

    app.setup_extension('sphinxnotes.render')

    app.add_config_value(
        'recentupdate_exclude_commit', ['skip-recentupdate'], 'env', types=list[str]
    )
    app.add_config_value('recentupdate_count', 10, 'env', types=int)
    app.add_config_value(
        'recentupdate_group_by', None, 'env', types=ENUM(None, 'day', 'month', 'year')
    )

    return meta.post_setup(app)
