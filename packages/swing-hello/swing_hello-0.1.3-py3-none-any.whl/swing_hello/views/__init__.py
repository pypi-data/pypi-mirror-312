# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Views Module
============

This module consolidates all view functions and classes used in the Swing Hello
application. It includes views for handling basic HTTP responses, rendering
templates, processing forms, and returning JSON responses.

Imported Views:
---------------

- hello_response_view (function-based view): Returns a basic HTTP response.
- HelloResponseView (class-based view): Returns a basic HTTP response.
- hello_template_view (function-based view): Renders a template with context.
- HelloTemplateView (class-based view): Renders a template with context.
- hello_form_view (function-based view): Handles form processing.
- HelloFormView (class-based view): Handles form processing.
- hello_json_view (function-based view): Returns a JSON response.
- HelloJsonView (class-based view): Returns a JSON response.

These views demonstrate basic responses, template rendering, form processing,
and JSON responses in Django.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Local Modules
from .view_hello_form import hello_form_view, HelloFormView
from .view_hello_json import hello_json_view, HelloJsonView
from .view_hello_response import hello_response_view, HelloResponseView
from .view_hello_template import hello_template_view, HelloTemplateView


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "hello_response_view",
    "HelloResponseView",
    "hello_template_view",
    "HelloTemplateView",
    "hello_form_view",
    "HelloFormView",
    "hello_json_view",
    "HelloJsonView",
]
