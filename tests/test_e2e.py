"""E2E tests for sphinxnotes.recentupdate extension."""

import pytest


@pytest.mark.sphinx('html', testroot='recentupdate-basic')
def test_recentupdate_basic(app, status, warning):
    app.build()

    html = (app.outdir / 'index.html').read_text(encoding='utf-8')

    # Second commit adds index.rst.
    assert 'Commit: Second commit: add index' in html
    # Root commit only adds conf.py (not a source file), so no doc changes.
    assert 'Commit: First commit: add conf' not in html


@pytest.mark.sphinx('html', testroot='recentupdate-path-filter')
def test_recentupdate_path_filter(app, status, warning):
    app.build()

    html = (app.outdir / 'index.html').read_text(encoding='utf-8')

    # path='subdir' filters to only commits touching subdir/
    assert 'Commit: Second commit: add subdir/doc' in html
    assert 'Commit: Third commit: add other' not in html
    assert 'Commit: First commit: add files' not in html


@pytest.mark.sphinx('html', testroot='recentupdate-current-doc')
def test_recentupdate_current_doc_filter(app, status, warning):
    app.build()

    html = (app.outdir / 'index.html').read_text(encoding='utf-8')

    # current_doc=True: only commits touching index.rst
    # Root commit only adds conf.py (no docs); second adds other.rst (not index.rst).
    assert 'Commit: Third commit: modify index' in html
    assert 'Commit: Second commit: add other' not in html
    assert 'Commit: First commit: add conf' not in html
