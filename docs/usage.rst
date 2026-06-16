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
  Number of recent revisions to return (default ``10``).

``path``
  A git pathspec (:manpage:`gitglossary(7)`) to filter file changes
  (default ``'.'``).
  See also :example:`Recent Updates of Custom Path`.

``current_doc``
  If ``True``, only return revisions that modified the current document
  (default ``False``).
  See also :example:`Recent Updates to Current Document`.

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

      {% for r in load_extra('recentupdate', count=5, path='docs/index.rst') %}
      ``{{ r.date }}`` — {{ r.message[0] }}
      {% endfor %}

.. example:: Recent Updates to Current Document

   .. data.render::

      Recent changes to this document:

      {% for r in load_extra('recentupdate', count=5, current_doc=True) %}
      ``{{ r.date }}`` — {{ r.message[0] }}
      {% endfor %}

``sphinxnotes-render``
======================

For more details about ``sphinxnotes-render``:

.. seealso::

   :external+render:doc:`sphinxnotes-render: Templating <tmpl>`
     How to write ``data.render`` templates.
   :external+render:doc:`sphinxnotes-render: Templating <ext>`
     How extra context and filters work.
