# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from __future__ import annotations

import sys
from pathlib import Path

project = 'Metadata Generator for the Alaska Energy Data Gateway'
copyright = '2025, Alaska Center for Energy and Power'
author = 'Alaska Center for Energy and Power'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.insert(0, Path.resolve(Path('../..')))

extensions = [
    "sphinx.ext.napoleon",
    "myst_parser",
    "autoapi.extension"
]

source_suffix = ['.rst', '.md']

templates_path = ['_templates']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'

html_sidebars = {
    "**": []
}

html_static_path = ['_static']

html_css_files = [
    'css/custom.css',
]

html_context = {
    "default_mode": "light"
}

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/acep-aedg",
            "icon": "fa-brands fa-github",
        }
    ],
    "logo": {
        "image_light": "_static/acep-logo-light.png",
        "image_dark": "_static/acep-logo-dark.png"
    },
    "pygments_light_style": "murphy",
    "pygments_dark_style": "nord",
    "navbar_end": ["navbar-icon-links"],
    "footer_start": [],
    "footer_center": ["nds", "copyright"],
    "footer_end": []
}

# -- Options for autoapi -------------------------------------------------------
autoapi_type = "python"
autoapi_dirs = ["../../src/aedg_metadata"]
autoapi_keep_files = True
autoapi_root = "api"
autoapi_member_order = "groupwise"
autoapi_ignore = ["*/.venv/*"]
