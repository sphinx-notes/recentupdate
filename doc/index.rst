========================
sphinxnotes.recentupdate
========================

.. image:: https://img.shields.io/github/stars/sphinx-notes/recentupdate.svg?style=social&label=Star&maxAge=2592000
   :target: https://github.com/sphinx-notes/recentupdate

:version: |version|
:copyright: Copyright ©2021 by Shengyu Zhang.
:license: BSD, see LICENSE for details.

Sphinx extension for generating a list of recently updated documents from git log, outputted as both document and RSS.

.. contents::
   :local:
   :backlinks: none

Installation
============

Download it from official Python Package Index:

.. code-block:: console

   $ pip install sphinxnotes-recentupdate

Add extension to :file:`conf.py` in your sphinx project:

.. code-block:: python

    extensions = [
              # …
              'sphinxnotes.recentupdate',
              # …
              ]

.. _Configuration:

Configuration
=============

The extension provides the following configuration:

Functionalities
===============

Change Log
==========

2021-XX-XX 1.0a0
----------------

PASS.
