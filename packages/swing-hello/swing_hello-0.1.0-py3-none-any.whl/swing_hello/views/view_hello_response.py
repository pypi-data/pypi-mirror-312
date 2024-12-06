# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Hello Response Views Module
===========================

Provides hello_response_view function and HelloResponseView class.

This module defines a simple function-based view and a class-based view to 
return a "Hello!" response. These views can be used to demonstrate basic 
Django view functionality.

Functions:
    - hello_response_view: A simple function-based view that returns "Hello!".

Classes:
    - HelloResponseView: A class-based view that returns "Hello!" on GET
      request.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Dict

# Import | Libraries
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.utils.translation import gettext as _

# Import | Local Modules


# =============================================================================
# Function
# =============================================================================

def hello_response_view(
    request: HttpRequest,
) -> HttpResponse:
    """
    Hello Response View Function
    ============================

    A simple function-based view that returns a plain text "Hello!" response.

    Parameters:
        - request (HttpRequest): The HTTP request object.

    Returns:
        - HttpResponse: A response object with "Hello!" text.

    """

    context: str = _("Hello!")

    return HttpResponse(
        context,
        content_type = "text/plain"
    )


# =============================================================================
# Class
# =============================================================================

class HelloResponseView(View):
    """
    Hello Response View Class
    =========================

    A class-based view that returns a plain text "Hello!" response on a
    GET request.

    Methods:
        - get(request, *args, **kwargs): Handles GET requests and returns
          "Hello!" text.

    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any],
    ) -> HttpResponse:
        """
        Handles GET requests and returns a plain text "Hello!" response.

        Parameters:
            - request (HttpRequest): The HTTP request object.
            - *args (Any): Variable length argument list.
            - **kwargs (Dict[str, Any]): Arbitrary keyword arguments.

        Returns:
            - HttpResponse: A response object with "Hello!" text.
        """

        context: str = _("Hello!")

        return HttpResponse(
            context,
            content_type = "text/plain"
        )


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "hello_response_view",
    "HelloResponseView",
]
