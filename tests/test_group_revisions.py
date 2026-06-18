import unittest
from collections import OrderedDict
from datetime import datetime, timezone

from sphinxnotes.recentupdate import (
    Revision,
    get_time_period_key,
    compact_revision,
    group_revisions,
    compact_groups,
)


def _make_rev(
    message: list[str],
    author: str,
    date: datetime,
    added: list[str] | None = None,
    changed: list[str] | None = None,
    removed: list[str] | None = None,
) -> Revision:
    return Revision(
        message=message,
        author=author,
        date=date,
        added_docs=added or [],
        changed_docs=changed or [],
        removed_docs=removed or [],
    )


def _group_and_compact(revs: list[Revision], group_by: str) -> list[Revision]:
    groups: OrderedDict[tuple[str, datetime], list[Revision]] = OrderedDict()
    for rev in revs:
        group_revisions(groups, rev, group_by)
    return compact_groups(groups)


class TestGetTimePeriodKey(unittest.TestCase):
    def test_day(self):
        dt = datetime(2024, 3, 15, 14, 30, 45, tzinfo=timezone.utc)
        result = get_time_period_key(dt, 'day')
        self.assertEqual(result, datetime(2024, 3, 15, 0, 0, 0, tzinfo=timezone.utc))

    def test_month(self):
        dt = datetime(2024, 3, 15, 14, 30, 45, tzinfo=timezone.utc)
        result = get_time_period_key(dt, 'month')
        self.assertEqual(result, datetime(2024, 3, 1, 0, 0, 0, tzinfo=timezone.utc))

    def test_year(self):
        dt = datetime(2024, 3, 15, 14, 30, 45, tzinfo=timezone.utc)
        result = get_time_period_key(dt, 'year')
        self.assertEqual(result, datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc))


class TestCompactRevision(unittest.TestCase):
    def test_single_revision(self):
        rev = _make_rev(['msg'], 'alice', datetime(2024, 1, 1, tzinfo=timezone.utc))
        result = compact_revision([rev])
        self.assertEqual(result.message, ['msg'])

    def test_merge_messages_and_files(self):
        rev1 = _make_rev(
            ['commit1'],
            'alice',
            datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc),
            added=['doc1'],
        )
        rev2 = _make_rev(
            ['commit2'],
            'alice',
            datetime(2024, 1, 1, 15, 0, tzinfo=timezone.utc),
            removed=['doc1'],
        )
        result = compact_revision([rev2, rev1])
        self.assertEqual(result.message, ['commit1', 'commit2'])
        self.assertEqual(result.added_docs, [])
        self.assertEqual(result.removed_docs, ['doc1'])


class TestGroupRevisions(unittest.TestCase):
    def test_same_author_same_day_groups(self):
        rev1 = _make_rev(
            ['c1'], 'alice', datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
        )
        rev2 = _make_rev(
            ['c2'], 'alice', datetime(2024, 1, 1, 15, 0, tzinfo=timezone.utc)
        )
        result = _group_and_compact([rev2, rev1], 'day')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, datetime(2024, 1, 1, tzinfo=timezone.utc))

    def test_different_author_not_grouped(self):
        rev1 = _make_rev(
            ['c1'], 'alice', datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
        )
        rev2 = _make_rev(
            ['c2'], 'bob', datetime(2024, 1, 1, 15, 0, tzinfo=timezone.utc)
        )
        result = _group_and_compact([rev2, rev1], 'day')
        self.assertEqual(len(result), 2)

    def test_different_day_not_grouped(self):
        rev1 = _make_rev(
            ['c1'], 'alice', datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
        )
        rev2 = _make_rev(
            ['c2'], 'alice', datetime(2024, 1, 2, 10, 0, tzinfo=timezone.utc)
        )
        result = _group_and_compact([rev1, rev2], 'day')
        self.assertEqual(len(result), 2)

    def test_merge_by_month(self):
        rev1 = _make_rev(['c1'], 'alice', datetime(2024, 1, 5, tzinfo=timezone.utc))
        rev2 = _make_rev(['c2'], 'alice', datetime(2024, 1, 20, tzinfo=timezone.utc))
        result = _group_and_compact([rev1, rev2], 'month')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, datetime(2024, 1, 1, tzinfo=timezone.utc))


if __name__ == '__main__':
    unittest.main()
