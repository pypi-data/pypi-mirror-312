# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Hello Template Views Module
===========================

Provides hello_template_view function and HelloTemplateView class.

This module defines a simple function-based view and a class-based view that 
renders a template with a context. These views can be used to demonstrate basic 
Django view functionality with templates.

Functions:
    - hello_template_view: A function-based view that renders a template with
      a context.

Classes:
    - HelloTemplateView: A class-based view that renders a template with
      a context.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Dict

# Import | Libraries
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.translation import gettext as _

# Import | Local Modules


# =============================================================================
# Function
# =============================================================================

def hello_template_view(
    request: Any,
) -> Any:
    """
    Hello Template View Function
    ============================

    A function-based view that renders a template with a given context.

    Parameters:
        - request (HttpRequest): The HTTP request object.

    Returns:
        - HttpResponse: A response object that renders the 'hello.html'
          template with the provided context.

    """

    context: Dict[str, str] = {
        "title": _("Hello!"),
        "content": "Lorem ipsum dolor sit amet",
    }
    return render(request, "swing_hello/hello_template.html", context)


# =============================================================================
# Class
# =============================================================================

class HelloTemplateView(TemplateView):
    """
    Hello Template View Class
    =========================

    A class-based view that renders a template with a given context.

    Attributes:
        - template_name (str): The name of the template to be rendered.

    """

    template_name = "swing_hello/hello_template.html"

    def get_context_data(
        self,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Returns context for rendering the template.

        Parameters:
            - *args (Any): Variable length argument list.
            - **kwargs (Dict[str, Any]): Arbitrary keyword arguments.

        Returns:
            - dict: A dictionary containing context data for the template.

        """

        context: Dict[str, Any] = super().get_context_data(**kwargs)

        context["title"] = _("Hello!")
        context["content"] = "Lorem ipsum dolor sit amet"

        return context


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "hello_template_view",
    "HelloTemplateView",
]
