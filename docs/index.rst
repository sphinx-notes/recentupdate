.. This file is generated from sphinx-notes/cookiecutter.

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
   :target: https://pypistats.org/packages/sphinxnotes-recentupdate
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

Get the Sphinx document update information from Git repository.

This extension provides a :rst:dir:`recentupdate` directive that displays
recent document update information read from a Git repository. It also
integrates with :external+render:doc:`sphinxnotes-render <index>` by
providing an extra context for use in render templates.

.. INTRODUCTION END

Getting Started
===============

.. note::

   We assume you already have a Sphinx documentation project,
   if not, see `Getting Started with Sphinx`_.


First, download the extension from PyPI:

.. code-block:: console

   $ pip install sphinxnotes-recentupdate


Then, add the extension name to ``extensions`` configuration option in your
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

Now you can use the :rst:dir:`recentupdate` directive to displays the recent
updates of the our documentation.

.. example::

   .. recentupdate:: 3

Please refer to :doc:`usage` for more details.

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
   GitHub <https://github.com/sphinx-notes>
   Blog <https://silverrainz.me/blog/category/sphinx.html>
   PyPI <https://pypi.org/search/?q=sphinxnotes>

__ https://github.com/SilverRainZ
