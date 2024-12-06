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

- TestHelloTemplateView: Contains tests for `hello_template_view` and
`HelloTemplateView`.

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
from swing_hello.views.view_hello_template import (
    hello_template_view,
    HelloTemplateView,
)


# =============================================================================
# Test Classes
# =============================================================================

@pytest.mark.django_db
class TestHelloTemplateView:
    """
    TestHelloTemplateView
    =====================

    Test suite for the `hello_template_view` and `HelloTemplateView` views.

    This class includes tests for GET requests to ensure that the views render 
    the correct template with the expected content.
    """

    def setup_method(self) -> None:
        """
        Setup Method
        ============

        Initializes the RequestFactory for use in test methods.

        The RequestFactory is used to simulate GET requests in the test
        methods.
        """
        self.factory: RequestFactory = RequestFactory()

    def test_hello_template_view_function(self) -> None:
        """
        Test hello_template_view Function (GET Request)
        ===============================================

        Tests GET request handling for the `hello_template_view`
        function-based view.

        Ensures that the function-based view renders the correct template 
        and includes the expected content "Hello!" and "Lorem ipsum dolor
        sit amet".

        Assertions:
        -----------
        - The response status code should be 200 (OK).
        - The response content should include "Hello!" and "Lorem ipsum dolor
          sit amet".
        """
        request: HttpRequest = self.factory.get("/hello/template")
        response: HttpResponse = hello_template_view(request)

        assert response.status_code == 200
        assert _("Hello!") in response.content.decode()
        assert "Lorem ipsum dolor sit amet" in response.content.decode()

    def test_hello_template_view_class(self) -> None:
        """
        Test HelloTemplateView Class (GET Request)
        ==========================================

        Tests GET request handling for the `HelloTemplateView` class-based
        view.

        Ensures that the class-based view renders the correct template 
        and includes the expected content "Hello!" and "Lorem ipsum dolor sit
        amet".

        Assertions:
        -----------
        - The response status code should be 200 (OK).
        - The response content should include "Hello!" and "Lorem ipsum dolor
        sit amet".
        """
        request: HttpRequest = self.factory.get("/hello/template")
        response: HttpResponse = HelloTemplateView.as_view()(request)

        assert response.status_code == 200
        assert _("Hello!") in response.content.decode()
        assert "Lorem ipsum dolor sit amet" in response.content.decode()


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "TestHelloTemplateView",
]
