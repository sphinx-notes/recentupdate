.. This file is generated from sphinx-notes/cookiecutter.

==========
Change Log
==========

.. hint:: You may want to learn about our `Release Strategy`__

   __ https://sphinx.silverrainz.me/release.html

.. Example:

   1.0
   ===

   .. version:: _
      :date: yyyy-mm-dd

   Change log here.

Version 2.x
===========

.. version:: 2.1
   :date: 2026-06-22

   - feat: The :rst:dir:`recentupdate:paths` is relative to srcdir
     (prefixed with ``/``) or current document (prefixed with ``.`` or no prefix)
     now
   - fix: Make sure all docnames in Revision prefixed with a ``/``,
     so it can be correctly referenced by Sphinx's :rst:role:`doc` role

.. version:: 2.0
   :date: 2026-06-22
   :break:

   - The template feature is now provided by
     :external+render:doc:`sphinxnotes-render <index>`. It offers richer features;
     Please see :external+render:doc:`tmpl`
   - The :rst:dir:`recentupdate` directive supports more options:

     - New ``:self:`` option: show only revisions that modified the
       current document
     - New ``:paths:`` option: Specifiy pathspecs to filter file changes
     - New ``:group-by:`` option: group revisions by time period (day/month/year)

   - Provide a ``recentupdate`` extra context for use within
     ``sphinxnotes-render`` compatible templates
   - New confval: ``recentupdate_group_by``

   BREAKING CHANGES:

   - Drop the ``strftime`` filters, use ``datetime.strfime`` instead
   - The ``roles`` filter is now provided by ``sphinxnotes-render``
   - Drop the ``recentupdate_exclude_path``, ``recentupdate_date_format`` confval
   - The members of :py:class:`~sphinxnotes.recentupdate.Revision` are renamed
   - Rename confval ``recentupdate_exclude_commit`` to ``recentupdate_skip_commit``

Version 1.x
===========

.. version:: 1.1
   :date: 2025-10-30

   - fix: Deal with case when sphinx srcdir != git workdir

.. version:: 1.0
   :date: 2025-10-17

   First stable version after five years :-)

.. version:: 1.0a0
   :date: 2021-12-06 

   Release alpha version.
