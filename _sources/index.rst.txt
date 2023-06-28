Sphinx-Cache Docs
=================

Sphinx-Cache is a `Sphinx <https://www.sphinx-doc.org>`_ extension for storing and restoring the `.doctrees` cache.

.. _install:

Installation
------------
We recommend using the latest version of Python. Sphinx-Cache supports Python 3.6 and newer versions.

.. tab-set::

    .. tab-item:: Using pip

        .. code-block:: bash

           $ pip install sphinx-cache

    .. tab-item:: From source

        .. code-block:: bash

           $ git clone https://github.com/useblocks/sphinx-cache
           $ cd sphinx-cache
           $ pip install .

.. _config:

Configuration
-------------

All configurations take place in your project's ``conf.py`` file.

Activation
**********

Add **sphinx_cache** to the extensions list.

.. code-block:: python

   extensions = ["sphinx_cache",]

Options
*******

All configuration options start with the prefix ``cache_`` for **Sphinx-Cache**.

.. _cache_store_path:

cache_store_path
++++++++++++++++

The ``cache_store_path`` option specifies the directory path where you want to save the doctree cache files.

.. note::

   The path should be specified as a relative path relative to the directory of the ``conf.py`` file.
    For example: :python:`cache_store_path = '.cache/'`.

Default: ``.cache/``

.. _cache_doctree_path:

cache_doctree_path
++++++++++++++++++

The ``cache_doctree_path`` option specifies the directory path of the doctree folder.

.. note::

   * The path should be specified as a relative path relative to the directory of the ``conf.py`` file.
     For example: :python:`cache_doctree_path = '_build/.doctrees'`.
   * We use the value provided for the ``cache_doctree_path`` as directory for storing pickled doctrees.
     If you don't specify the value for the ``cache_doctree_path`` in the ``conf.py`` file, we use the default
     value for the ``cache_doctree_path`` (i.e. ``_build/.doctrees``).

Default: ``_build/.doctrees``

.. toctree::
   :maxdepth: 2
   :hidden:

   Changelog <changelog>
   Support <support>