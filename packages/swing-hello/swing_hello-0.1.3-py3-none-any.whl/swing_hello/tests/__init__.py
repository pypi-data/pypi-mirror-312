# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Hello Tests Module
==================

This module consolidates the test cases for the Swing Hello application. It
includes test classes for form handling, JSON responses, template rendering,
and basic HTTP response handling.

Modules:
--------

- TestHelloFormView: Tests for form views.
- TestHelloJsonView: Tests for JSON response views.
- TestHelloResponseView: Tests for basic HTTP response views.
- TestHelloTemplateView: Tests for template rendering views.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Local Modules
from .test_view_hello_form import TestHelloFormView
from .test_view_hello_json import TestHelloJsonView
from .test_view_hello_response import TestHelloResponseView
from .test_view_hello_template import TestHelloTemplateView


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "TestHelloFormView",
    "TestHelloJsonView",
    "TestHelloResponseView",
    "TestHelloTemplateView",
]
