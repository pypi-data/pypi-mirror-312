# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
#
#

# -- How to
# cd docs
# sphinx-apidoc -f -o source/ ../swotted/
# make html

import os
import sys


src = os.path.abspath("../..")
sys.path.insert(0, src)  # location of the sources
os.environ["PYTHONPATH"] = src  # <- this way seems required by nbsphinx


# -- Project information -----------------------------------------------------

project = "SWoTTeD"
copyright = "2023, Hana Sebia, Thomas Guyet and Mike Rye"
author = "Hana Sebia, Thomas Guyet and Mike Rye"


# -- General configuration ---------------------------------------------------
autodoc_mock_imports = [
    "omegaconf",
    "lightning",
    "hydronaut",
]

extensions = [
    "sphinx.ext.napoleon",  # Parse NumPy docstrings syntax
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_rtd_theme",
    "nbsphinx",  # use jupyter notebooks
    "sphinx.ext.mathjax",
    "myst_parser",  # used to use both Markdown and RST files
]

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

intersphinx_mapping = {
    "rtd": ("https://docs.readthedocs.io/en/stable/", None),
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "torch": ("https://pytorch.org/docs/stable/", None),
}
intersphinx_disabled_domains = ["std"]

# -- Options for EPUB output
epub_show_urls = "footnote"

templates_path = ["_templates"]
exclude_patterns = ["_build", "tests", "experiments"]

## -- nbsphinx settings --

nbsphinx_execute = "never"  # block execution of notebooks

# "".ipynb_checkpoints" are excluded automatically by nbsphinx


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# disable docstring in Google style (the project uses NumPy style)
napoleon_google_docstring = False
