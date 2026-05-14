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

.. version:: 2.0
   :break:

   - Integrated with :external+render:doc:`sphinxnotes-render <index>`
   - Drop the ``.. recentupdate::`` directive, use ``load_extra('recentupdates')``
     in :rst:dir:`data.render`'s template
   - Drop the ``recentupdate_date_format`` confval

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
