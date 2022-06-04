# Fixed https://github.com/Whoeza/html_and_py/issues/8
from .html_and_py import (
    HTML_PROTOTYPE,
    HTML_VOID_ELEMENTS,
    create_html,
    init_doctype,
    is_self_enclosing,
    render_html,
    update_html
)

__all__ = [
    "HTML_PROTOTYPE",
    "HTML_VOID_ELEMENTS",
    "create_html",
    "init_doctype",
    "is_self_enclosing",
    "render_html",
    "update_html"
]
