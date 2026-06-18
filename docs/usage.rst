=====
Usage
=====

The extension provides an extra context ``recentupdate`` for `sphinxnotes-render`_.
Extra context can be load by the :external+render:term:`load_extra` function in
a Jinja template. User can easily render a Jinja template via :rst:dir:`data.render`
directive.

``recentupdate``
================

When calling ``load_extra('recentupdate', **kwargs)`` in the template, the
following parameters are available:

``count``
  Number of recent revisions to return (default from :confval:`recentupdate_count`).

``paths``
  A list of git pathspecs (:manpage:`gitglossary(7)`) to filter file changes
  (default ``['.']``).
  See also :example:`Recent Updates of Custom Path`.

``current_doc``
  If ``True``, only return revisions that modified the current document
  (default ``False``). When enabled, ``paths`` is overridden with a pathspec
  matching the current document.
  See also :example:`Recent Updates to Current Document`.

.. note::

   ``paths`` and ``current_doc`` are mutually exclusive. When ``current_doc=True``,
   the ``paths`` parameter is ignored.

.. role:: py(code)
  :language: Python

``group_by``
  Group revisions by time period. Revisions are grouped by UTC time
  period and author.

  Default from :confval:`recentupdate_group_by`, Available values:
  :data.render:`{{ load_extra('env').config.values['recentupdate_group_by'].valid_types | autoconfval_types | join(', ') }}`.

  See also :example:`Grouped Recent Updates`.

Each item returned is a :py:class:`~sphinxnotes.recentupdate.Revision` object:

.. autoclass:: sphinxnotes.recentupdate.Revision

   .. autoattribute:: message
   .. autoattribute:: author
   .. autoattribute:: date
   .. autoattribute:: added_docs
   .. autoattribute:: changed_docs
   .. autoattribute:: removed_docs

This is a basic example:

.. example::

   .. data.render::

      {% for r in load_extra('recentupdate', count=5) %}
      ``👤{{ r.author }}`` @ ``📅 {{ r.date }}``
         {{ r.message[0] }}
      {% endfor %}

Examples
========

.. example:: Show Which Files Updated

   .. data.render::

      {% for r in load_extra('recentupdate', count=5) %}
      ``📅 {{ r.date }}``
         {% if r.changed_docs -%}
         :Modified: {{ r.changed_docs | roles("doc") | join(", ") }}
         {% endif %}
         {% if r.added_docs -%}
         :Added: {{ r.added_docs | roles("doc") | join(", ") }}
         {% endif %}
         {% if r.removed_docs -%}
         :Deleted: {{ r.removed_docs | join(", ") }}
         {% endif %}
      {% endfor %}

      The aboved :external+render:term:`roles` filter is also provided by
      `sphinxnotes-render`_.

.. example:: Recent Updates of Custom Path

   .. data.render::

      Recent changes of the ``docs/index.rst`` file:

      {% for r in load_extra('recentupdate', count=5, paths=['docs/index.rst']) %}
      ``{{ r.date }}`` — {{ r.message[0] }}
      {% endfor %}

.. example:: Recent Updates to Current Document

   .. data.render::

      Recent changes to this document:

      {% for r in load_extra('recentupdate', count=5, current_doc=True) %}
      ``{{ r.date }}`` — {{ r.message[0] }}
      {% endfor %}

.. example:: Grouped Recent Updates

   .. data.render::

      Recent updates grouped by day:

      {% for r in load_extra('recentupdate', count=10, group_by='month') %}
      ``📅 {{ r.date.strftime('%Y-%m') }}``
         {% for msg in r.message[:3] %}
         {{ msg }}
         {% endfor %}
      {% endfor %}

``sphinxnotes-render``
======================

For more details about ``sphinxnotes-render``:

.. seealso::

   :external+render:doc:`sphinxnotes-render: Templating <tmpl>`
     How to write ``data.render`` templates.
   :external+render:doc:`sphinxnotes-render: Extending <ext>`
     How extra context and filters work.
