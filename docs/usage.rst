=====
Usage
=====

The :rst:dir:`recentupdate` directive is the recommended way to display recent
document updates. For cases where you need recent update information inside a
`sphinxnotes-render`_ compatible template (e.g. alongside other extra contexts),
use the ``recentupdate`` extra context instead.

The ``recentupdate`` Directive
==============================

.. rst:directive:: .. recentupdate:: [count]

   Display recent document updates from Git.

   The optional ``count`` is the number of recent revisions to display.
   Defaults to :confval:`recentupdate_count`.

   .. rst:directive:option:: self
      :type: flag

      Only show revisions that modified the current document.
      Mutually exclusive with :rst:dir:`recentupdate:paths`.

      See also :example:`Recent Updates to Current Document`.

   .. rst:directive:option:: paths
      :type: lines of str

      Git pathspecs (:manpage:`gitglossary(7)`) to filter file changes,
      one per line. Defaults to ``.``.

      See also :example:`Recent Updates of Custom Path`.

   .. rst:directive:option:: group-by
      :type: str

      .. role:: py(code)
        :language: Python

      Group revisions by time period.
      Available values:
      :data.render:`{{ load_extra('env').config.values['recentupdate_group_by'].valid_types | autoconfval_types | join(', ') }}`.
      Defaults to :confval:`recentupdate_group_by`.

      See also :example:`Grouped Recent Updates`.

   The directive body is a Jinja2 template. When empty,
   :confval:`recentupdate_template` is used. The template context contains
   a ``{{ revisions }}`` variable, it is a list of
   :py:class:`~sphinxnotes.recentupdate.Revision` objects.

.. autoclass:: sphinxnotes.recentupdate.Revision

   .. autoattribute:: message
   .. autoattribute:: author
   .. autoattribute:: date
   .. autoattribute:: added_docs
   .. autoattribute:: changed_docs
   .. autoattribute:: removed_docs

This is a basic example using the default template:

.. example::

   .. recentupdate::

The ``recentupdate`` Extra Context
==================================

.. tip::

   The extra context is for use within `sphinxnotes-render`_ compatible templates.
   In most cases, prefer the :rst:dir:`recentupdate` directive instead.

The ``recentupdate`` extra context can be loaded via
:external+render:term:`load_extra` in a Jinja template
(e.g. via :rst:dir:`data.render`):

Parameters:

``count``
   Equivalent to the argument of :rst:dir:`recentupdate`.

``paths``
   Equivalent to :rst:dir:`recentupdate:paths`.

``self_only``
   Equivalent to :rst:dir:`recentupdate:self`.

``group_by``
   Equivalent to :rst:dir:`recentupdate:group-by`.

                    
This is a basic example:

.. example::

   .. data.render::

      {% for r in load_extra('recentupdate', count=5) %}
      ``👤 {{ r.author }}`` @ ``📅 {{ r.date.strftime('%Y-%m-%d') }}``::

         {{ r.message[0] }}
      {% endfor %}

.. note:: To Use the ``data.render`` directive, you need to add
   ``sphinxnotes.render.ext`` to your Sphinx extension list.

Examples
========

.. example:: Show Which Documents Updated

   .. recentupdate::

      {% for r in revisions %}
      ``{{ r.date.strftime('%Y-%m-%d') }}``
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

   Recent changes of the :doc:`changelog`:

   .. recentupdate::
      :paths: docs/changelog.rst

      {% for r in revisions %}
      ``{{ r.date.strftime('%Y-%m-%d') }}`` — {{ r.message[0] }}
      {% endfor %}

.. example:: Recent Updates to Current Document

   Recent changes to this document:

   .. recentupdate::
      :self:

      {% for r in revisions %}
      ``{{ r.date.strftime('%Y-%m-%d') }}`` — {{ r.message[0] }}
      {% endfor %}

.. example:: Grouped Recent Updates

   Recent updates grouped by month:

   .. recentupdate:: 3
      :group-by: month

      {% for r in revisions %}
      ``📅 {{ r.date.strftime('%Y-%m') }}``
         ::
            {% for msg in r.message[:20] %}
            {{ msg }}
            {%- endfor %}
            ...
      {% endfor %}

``sphinxnotes-render``
======================

For more details about ``sphinxnotes-render``:

.. seealso::

   :external+render:doc:`sphinxnotes-render: Templating <tmpl>`
     How to write ``data.render`` templates.
   :external+render:doc:`sphinxnotes-render: Extending <ext>`
     How extra context and filters work.
