import unittest
from unittest.mock import MagicMock

from sphinxnotes.recentupdate import _resolve_paths


def _make_repo(working_dir='/srv/repo'):
    repo = MagicMock()
    repo.working_dir = working_dir
    return repo


def _make_env(srcdir='/srv/repo/docs'):
    env = MagicMock()
    env.srcdir = srcdir

    def doc2path(docname):
        return f'{srcdir}/{docname}.rst'

    env.doc2path = doc2path
    return env


class TestResolvePaths(unittest.TestCase):
    def test_absolute_path_resolves_relative_to_srcdir(self):
        """Paths starting with '/' are relative to srcdir."""
        repo = _make_repo('/srv/repo')
        env = _make_env('/srv/repo/docs')
        result = _resolve_paths(repo, env, 'index', ['/subdir/page'])
        self.assertEqual(result, ['docs/subdir/page'])

    def test_relative_path_resolves_relative_to_doc_dir(self):
        """Paths without prefix are relative to current document's directory."""
        repo = _make_repo('/srv/repo')
        env = _make_env('/srv/repo/docs')
        result = _resolve_paths(repo, env, 'subdir/index', ['other'])
        self.assertEqual(result, ['docs/subdir/other'])

    def test_dot_slash_path_resolves_relative_to_doc_dir(self):
        """Paths starting with './' are relative to current document's directory."""
        repo = _make_repo('/srv/repo')
        env = _make_env('/srv/repo/docs')
        result = _resolve_paths(repo, env, 'subdir/index', ['./other'])
        self.assertEqual(result, ['docs/subdir/other'])

    def test_root_doc_relative_path(self):
        """Relative path from root document resolves correctly."""
        repo = _make_repo('/srv/repo')
        env = _make_env('/srv/repo/docs')
        result = _resolve_paths(repo, env, 'index', ['page'])
        self.assertEqual(result, ['docs/page'])

    def test_empty_paths(self):
        """Empty paths list returns empty list."""
        repo = _make_repo('/srv/repo')
        env = _make_env('/srv/repo/docs')
        result = _resolve_paths(repo, env, 'index', [])
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
