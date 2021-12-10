========================
sphinxnotes.recentupdate
========================

.. image:: https://img.shields.io/github/stars/sphinx-notes/recentupdate.svg?style=social&label=Star&maxAge=2592000
   :target: https://github.com/sphinx-notes/recentupdate

:version: |version|
:copyright: Copyright ©2021 by Shengyu Zhang.
:license: BSD, see LICENSE for details.

Get the document update information from git and display it in Sphinx documentation.

This extensions provides a `recentupdate <Functionalities>`_ directive, which can show recent document update of current Sphinx documentation. The update information is read from Git_ repository (So you must use Git to manage your documentation). You can customize the update information through generating reStructuredText from Jinja_ template.

.. _Git: https://git-scm.com/
.. _Jinja: https://jinja.palletsprojects.com/en/3.0.x/templates/

.. contents::
   :local:
   :backlinks: none

Installation
============

Download it from official Python Package Index:

.. code:: console

   $ pip install sphinxnotes-recentupdate

Add extension to :file:`conf.py` in your sphinx project:

.. code:: python

    extensions = [
              # …
              'sphinxnotes.recentupdate',
              # …
              ]

Quick Start
===========

1. Installation_
2. Add ``recentupdate`` directive to your document:

   .. code:: rst

      .. recentupdate::

3. Build your document, The directive will be rendered to:

   .. recentupdate::

Functionalities
===============

The extension provides a ``recentupdate`` directive:

.. code:: rst

   .. recentupdate:: [count]

      [jinja template]

count
   The optional argument of directive is the count of recent "revisions" you want to show. Revision is a git commit which contains document changes.

   If no count given, value of :confval:`recentupdate_count` is used.

template
   The optional content of directive is a jinja template for generating reStructuredText, in the template you can access Variables_ named `{{ revisions }}`_.

   Beside, You can use `Builtin Filters`_ and Filters_ provided by extensions.

   If no template given, value of :confval:`recentupdate_template` is used.

.. _Builtin Filters: https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-filters

Variables
---------

All available variables_:

.. _variables: https://jinja.palletsprojects.com/en/3.0.x/templates/#variables

{{ revisions }}
~~~~~~~~~~~~~~~

``{{ revisions }}`` is an an array of revisions. The length of array is determined by the argument of`recentupdate <Functionalities>`_ directive.

Here is the schema of array element:

.. autoclass:: recentupdate.Revision
   :members:

Filters
-------

strftime
~~~~~~~~

Convert a :py:class:`datetime.datetime` to string in given format.

If no format given, use value of :confval:`recentupdate_date_format`.

It is used in :confval:`default template <recentupdate_template>`.

roles
~~~~~

Convert a list of string to list of reStructuredText roles.

``{{ ['foo', 'bar'] | roles("doc") }}`` produces ``[':doc:`foo`', ':doc:`bar`']``.

It is used in :confval:`default template <recentupdate_template>`.

Configuration
=============

The extension provides the following configuration:

.. confval:: recentupdate_count
   :type: int
   :default: 10

   The default count of recent revisions. See Functionalities_.

.. confval:: recentupdate_template
   :type: string
   :default: see below

   The default Jinja template of update information. See Functionalities_.

   Here is the default value:

   .. code:: jinja

      {% for r in revisions %}
      {{ r.date | strftime }}
        :Author: {{ r.author }}
        :Message: {{ r.message }}

        {% if r.modification %}
        - Modified {{ r.modification | roles("doc") | join(", ") }}
        {% endif %}
        {% if r.addition %}
        - Added {{ r.addition | roles("doc") | join(", ") }}
        {% endif %}
        {% if r.deletion %}
        - Deleted {{ r.deletion | join(", ") }}
        {% endif %}
      {% endfor %}

.. confval:: recentupdate_date_format
   :type: string
   :default: "%Y-%m-%dT"

   The default date format of strftime_ filter.

Change Log
==========

2021-12-06 1.0a0
----------------

Release alpha version.
