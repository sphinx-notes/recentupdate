=============
Configuration
=============

The extension provides the following configuration:

.. autoconfval:: recentupdate_exclude_commit

   A list of commit message pattern that should be excluded when looking for file changes.

.. autoconfval:: recentupdate_count

   Number of recent revisions to return by default when calling
   ``load_extra('recentupdate')`` without an explicit ``count`` parameter.
