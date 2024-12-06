# -- Project information -----------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))


project = 'AFusion'
copyright = '2024, Hanzi'
author = 'Hanzi'
release = '1.2.2'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'myst_parser',
]
# Enable Markdown support
source_suffix = ['.rst', '.md']
autoclass_content = 'both'
autodoc_member_order = 'bysource'

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# The theme to use for HTML and HTML Help pages.
html_theme = 'furo'
html_theme_options = {
    "sidebar_hide_name": False,  # 确保页面名称显示在侧边栏
}
html_static_path = ['_static']
