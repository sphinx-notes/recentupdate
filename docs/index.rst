.. This file is generated from sphinx-notes/cookiecutter.
   You need to consider modifying the TEMPLATE or modifying THIS FILE.

========================
sphinxnotes-recentupdate
========================

.. |docs| image:: https://img.shields.io/github/deployments/sphinx-notes/recentupdate/github-pages?label=docs
   :target: https://sphinx.silverrainz.me/recentupdate
   :alt: Documentation Status
.. |license| image:: https://img.shields.io/github/license/sphinx-notes/recentupdate
   :target: https://github.com/sphinx-notes/recentupdate/blob/master/LICENSE
   :alt: Open Source License
.. |pypi| image:: https://img.shields.io/pypi/v/sphinxnotes-recentupdate.svg
   :target: https://pypi.python.org/pypi/sphinxnotes-recentupdate
   :alt: PyPI Package
.. |download| image:: https://img.shields.io/pypi/dm/sphinxnotes-recentupdate
   :target: https://pypi.python.org/pypi/sphinxnotes-recentupdate
   :alt: PyPI Package Downloads
.. |github| image:: https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white/
   :target: https://github.com/sphinx-notes/recentupdate
   :alt: GitHub Repository

|docs| |license| |pypi| |download| |github|

Introduction
============

.. INTRODUCTION START

Get the document update information from git and display it in Sphinx documentation.

This extensions provides a :doc:`recentupdate <usage>` directive, which can show recent document update of current Sphinx documentation. The update information is read from Git_ repository (So you must use Git to manage your documentation). You can customize the update information through generating reStructuredText from Jinja_ template.

.. _Git: https://git-scm.com/
.. _Jinja: https://jinja.palletsprojects.com/en/3.0.x/templates/

.. INTRODUCTION END

Getting Started
===============

.. note::

   We assume you already have a Sphinx documentation,
   if not, see `Getting Started with Sphinx`_.


First, downloading extension from PyPI:

.. code-block:: console

   $ pip install sphinxnotes-recentupdate


Then, add the extension name to ``extensions`` configuration item in your
:parsed_literal:`conf.py_`:

.. code-block:: python

   extensions = [
             # …
             'sphinxnotes.recentupdate',
             # …
             ]

.. _Getting Started with Sphinx: https://www.sphinx-doc.org/en/master/usage/quickstart.html
.. _conf.py: https://www.sphinx-doc.org/en/master/usage/configuration.html

.. ADDITIONAL CONTENT START

Add ``recentupdate`` directive to your document, build your document, the directive will be rendered to:

.. example::
   :style: grid

   .. recentupdate::

.. ADDITIONAL CONTENT END

Contents
========

.. toctree::
   :caption: Contents

   usage
   conf
   changelog

The Sphinx Notes Project
========================

The project is developed by `Shengyu Zhang`__,
as part of **The Sphinx Notes Project**.

.. toctree::
   :caption: The Sphinx Notes Project

   Home <https://sphinx.silverrainz.me/>
   Blog <https://silverrainz.me/blog/category/sphinx.html>
   PyPI <https://pypi.org/search/?q=sphinxnotes>

__ https://github.com/SilverRainZ
