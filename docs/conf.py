# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Sphinx-Cache"
copyright = "2023, team useblocks"
author = "team useblocks"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_cache",
    "sphinx_design",
    "sphinx_immaterial",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_immaterial"
html_title = "Sphinx-Cache"
html_static_path = ["_static"]

rst_prolog = """
.. role:: bash(code)
   :language: bash

.. role:: python(code)
   :language: python

"""  # noqa: W293

# Sphinx-Cache Configuration
# cache_store_path = ""
# cache_doctree_path = ""
