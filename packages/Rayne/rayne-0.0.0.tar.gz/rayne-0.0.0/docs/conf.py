"""Configuration file for the Sphinx documentation builder."""

import sys
from pathlib import Path

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# pylint: disable=invalid-name
# cspell: words extlinks furo
# mypy: ignore-errors

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Rayne"
project_copyright = "2024, brobeson"
author = "brobeson"
version = "0.0.0"
release = "0.0.0"
highlight_language = "python"

sys.path.insert(0, str(Path("..", "rayne").resolve()))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_title = project
html_theme_options = {
    "dark_css_variables": {"color-announcement-background": "#ff5252"},
    # pylint: disable=line-too-long
    "announcement": 'This is alpha software. The interface is subject to breaking changes.<br/>You can see the pre-release road map at the <a href="https://github.com/users/brobeson/projects/6/views/1?filterQuery=milestone%3A%22Next+Release%22">kanban board</a>.',
}

copybutton_exclude = ".linenos, .gp, .go"
extlinks = {"issue": ("https://github.com/brobeson/Rayne/issues/%s", "issue %s")}
