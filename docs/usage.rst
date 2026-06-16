=====
Usage
=====

The extension provides an extra context ``recentupdate`` usable via
:external+render:term:`load_extra` function in ``sphinxnotes-render`` template:

.. example::

   .. data.render::

      {% for r in load_extra('recentupdate', 3) %}
      ``📅 {{ r.date }}`` | ``👤{{ r.author }}``

        {{ r.message[0] }}

      {% if r.changed_docs %}
      - Modified {{ r.changed_docs | roles("doc") | join(", ") }}
      {% endif %}
      {% if r.added_docs %}
      - Added {{ r.added_docs | roles("doc") | join(", ") }}
      {% endif %}
      {% if r.removed_docs %}
      - Deleted {{ r.removed_docs | join(", ") }}
      {% endif %}

      {% endfor %}

The ``load_extra('recentupdate', count=3)`` returns a list of
:py:class:`~sphinxnotes.recentupdate.Revision` objects from recent Git
commits that touched document files, see below.

The :external+render:term:`roles` filter is provided by ``sphinxnotes-render``
too.

.. example::

   .. data.render::

      Recent changes to this document:

      {% for r in load_extra('recentupdate', count=5, current_doc=True) %}
      ``{{ r.date }}`` — {{ r.message[0] }}
      {% endfor %}

.. example::

   .. data.render::

      Recent changes in the ``docs/`` directory:

      {% for r in load_extra('recentupdate', count=10, path='docs') %}
      ``{{ r.date }}`` — {{ r.message[0] }}
      {% endfor %}

.. seealso::

   :external+render:doc:`sphinxnotes-render: Templating <tmpl>`
     How to write ``data.render`` templates.
   :external+render:doc:`sphinxnotes-render: Templating <ext>`
     How extra context and filters work.

The "recentupdate" extra context
=================================

``load_extra('recentupdate', count=3)`` returns a list of
:py:class:`~sphinxnotes.recentupdate.Revision` objects from recent Git
commits that touched document files.

- ``count`` (*int*) — Number of recent revisions to return (default ``10``).
- ``path`` (*str*) — A :manpage:`pathspec(7)` to filter file changes
  (default ``'.'``, i.e., entire repository).
- ``current_doc`` (*bool*) — If ``True``, only return revisions that
  modified the current document (default ``False``).

.. py:class:: sphinxnotes.recentupdate.Revision

   .. autoattribute:: message

   .. autoattribute:: author

   .. autoattribute:: date

   .. autoattribute:: added_docs

   .. autoattribute:: changed_docs

   .. autoattribute:: removed_docs
