=====
Usage
=====

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
=========

All available variables_:

.. _variables: https://jinja.palletsprojects.com/en/3.0.x/templates/#variables

{{ revisions }}
---------------

``{{ revisions }}`` is an an array of revisions. The length of array is determined by the argument of`recentupdate <Functionalities>`_ directive.

Here is the schema of array element:

.. autoclass:: recentupdate.Revision
   :members:

Filters
=======

strftime
--------

Convert a :py:class:`datetime.datetime` to string in given format.

If no format given, use value of :confval:`recentupdate_date_format`.

It is used in :confval:`default template <recentupdate_template>`.

roles
-----

Convert a list of string to list of reStructuredText roles.

``{{ ['foo', 'bar'] | roles("doc") }}`` produces ``[':doc:`foo`', ':doc:`bar`']``.

It is used in :confval:`default template <recentupdate_template>`.
