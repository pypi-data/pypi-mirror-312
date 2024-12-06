# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Hello Form Tests Module
=======================

This module contains the test suite for the form-related views in the Swing Hello 
application. It includes tests for both the function-based and class-based views 
responsible for handling form submissions and rendering form pages.

Classes:
--------

- TestHelloFormView: Contains tests for `hello_form_view` and `HelloFormView`.

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
from swing_hello.views.view_hello_form import (
    hello_form_view,
    HelloFormView
)


# =============================================================================
# Test Classes
# =============================================================================

@pytest.mark.django_db
class TestHelloFormView:
    """
    Hello Form Tests Class
    ======================

    Test suite for the `hello_form_view` and `HelloFormView` views.

    This class includes tests for GET and POST requests to ensure that the 
    views behave as expected when rendering forms and processing form
    submissions.

    """

    def setup_method(self) -> None:
        """
        Setup the RequestFactory for use in test methods.

        The RequestFactory is used to simulate GET and POST requests in the
        test methods.
        """
        self.factory: RequestFactory = RequestFactory()

    def test_hello_form_view_function_get(self) -> None:
        """
        Test GET request handling for `hello_form_view`.

        Ensures that the view correctly renders the form page.
        """
        request: HttpRequest = self.factory.get("/hello/form_func")
        response: HttpResponse = hello_form_view(request)

        assert response.status_code == 200
        assert "form" in response.content.decode()

    def test_hello_form_view_function_post(self) -> None:
        """
        Test POST request handling for `hello_form_view`.

        Ensures that the view correctly processes the form submission and returns 
        a greeting message including the submitted name.
        """
        request: HttpRequest = self.factory.post(
            "/hello/form_func",
            {"name": "Alice"},
        )
        response: HttpResponse = hello_form_view(request)

        assert response.status_code == 200
        assert _("Hello, Alice!") in response.content.decode()

    def test_hello_form_view_class_get(self) -> None:
        """
        Test GET request handling for `HelloFormView`.

        Ensures that the class-based view correctly renders the form page.
        """
        request: HttpRequest = self.factory.get("/hello/form")
        response: HttpResponse = HelloFormView.as_view()(request)

        assert response.status_code == 200
        assert "form" in response.content.decode()

    def test_hello_form_view_class_post(self) -> None:
        """
        Test POST request handling for `HelloFormView`.

        Ensures that the class-based view correctly processes the form
        submission  and returns a greeting message including the submitted
        name.
        """
        request: HttpRequest = self.factory.post(
            "/hello/form",
            {"name": "Alice"},
        )
        response: HttpResponse = HelloFormView.as_view()(request)

        assert response.status_code == 200
        assert "Hello, Alice!" in response.content.decode()


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "TestHelloFormView",
]
