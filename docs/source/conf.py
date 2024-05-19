# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


project = 'ArgParseTyped'
copyright = '2024, Martin Scharrer'
author = 'Martin Scharrer'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
]

autosummary_generate = True
templates_path = ['_templates']
exclude_patterns = []


autodoc_class_signature = 'mixed'
autodoc_typehints = 'both'
autodoc_typehints_format = 'short'
add_module_names = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "classic"
# html_theme = 'alabaster'
html_static_path = ['_static']


intersphinx_mapping = {
	'python':         ('https://docs.python.org/3', None),
}
#  autodoc_member_order='bysource'

autodoc_default_flags = ['members', 'undoc-members', 'show-inheritance']
# [ 'members', 'undoc-members', 'private-members', 'special-members', 'inherited-members', 'show-inheritance']

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
