=============
Configuration
=============

The extension provides the following configuration:

.. autoconfval:: recentupdate_count

   Number of recent revisions to return by default.

.. autoconfval:: recentupdate_template

   Default Jinja2 template for the :rst:dir:`recentupdate` directive.
   Used when the directive has no body content.
   The template context contains ``revisions``, a list of
   :py:class:`~sphinxnotes.recentupdate.Revision` objects.

.. autoconfval:: recentupdate_exclude_commit

   A list of commit message pattern that should be excluded when looking for file changes.

.. autoconfval:: recentupdate_group_by

   Group revisions by time period. When set, revisions are grouped by
   UTC time period and author. Defaults to ``commit``, which means
   each commit is shown separately.
