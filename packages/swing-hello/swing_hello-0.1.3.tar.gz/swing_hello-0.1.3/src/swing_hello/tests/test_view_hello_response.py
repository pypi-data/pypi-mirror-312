# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Hello Views Tests Module
========================

This module contains the test suite for the various views in the Swing Hello 
application. It includes tests for function-based and class-based views that 
handle HTTP responses, template rendering, JSON responses, form processing, 
and API endpoints.

Classes:
--------

- TestHelloResponseView: Contains tests for `hello_response_view` and `
  HelloResponseView`.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any

# Import | Libraries
import pytest
from django.test import RequestFactory, HttpRequest
from django.http import HttpResponse
from django.utils.translation import gettext as _

# Import | Local Modules
from swing_hello.views.view_hello_response import (
    hello_response_view,
    HelloResponseView
)


# =============================================================================
# Test Classes
# =============================================================================

@pytest.mark.django_db
class TestHelloResponseView:
    """
    TestHelloResponseView
    =====================

    Test suite for the `hello_response_view` and `HelloResponseView` views.

    This class includes tests for GET requests to ensure that the views return 
    the correct HTTP responses with the expected content.
    """

    def setup_method(self) -> None:
        """
        Setup the RequestFactory for use in test methods.

        The RequestFactory is used to simulate GET requests in the test methods.
        """
        self.factory: RequestFactory = RequestFactory()

    def test_hello_response_view_function(self) -> None:
        """
        Test GET request handling for `hello_response_view`.

        Ensures that the function-based view returns the correct HTTP response 
        with the content "Hello!".
        """
        request: HttpRequest = self.factory.get("/hello/response")
        response: HttpResponse = hello_response_view(request)

        assert response.status_code == 200
        assert response.content.decode() == "Hello!"

    def test_hello_response_view_class(self) -> None:
        """
        Test GET request handling for `HelloResponseView`.

        Ensures that the class-based view returns the correct HTTP response 
        with the content "Hello!".
        """
        request: HttpRequest = self.factory.get("/hello/response")
        response: HttpResponse = HelloResponseView.as_view()(request)

        assert response.status_code == 200
        assert response.content.decode() == _("Hello!")


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "TestHelloResponseView",
]
