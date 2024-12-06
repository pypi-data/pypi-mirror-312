# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Hello Form Module
=================

This module defines the HelloForm class, which is used for collecting and
validating a user's name within the Swing Hello application.

The form includes custom validation to ensure that the provided name contains
only alphabetic characters and spaces.

Classes:
--------
- HelloForm: A Django form class for collecting and validating a user's name.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any

# Import | Libraries
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Import | Local Modules
# (No local imports required)


# =============================================================================
# Forms
# =============================================================================

class HelloForm(forms.Form):
    """
    Hello Form Class
    ================

    A form for collecting a user's name.

    Fields:
    -------
    - name (str): A CharField for the user's name, limited to 100 characters.

    Methods:
    --------
    - clean_name() -> str: Custom validation method to ensure the name
      contains only alphabetic characters and spaces.
    - save() -> str: Placeholder method for saving form data. Can be customized
      for additional processing, such as saving to a database or sending an
      email.

    """

    name: forms.CharField = forms.CharField(
        label = _("Your Name"),
        max_length = 100,
        required = True,
        widget = forms.TextInput(attrs={"placeholder": _("Enter your name")}),
        help_text = _("Please enter your full name."),
    )

    def clean_name(self) -> str:
        """
        Custom validation for the 'name' field.

        Ensures that the name contains only alphabetic characters and spaces.

        Returns:
        --------
        - str: The cleaned name if valid.

        Raises:
        -------
        - ValidationError: If the name contains non-alphabetic characters or
          symbols.
        """
        name: str = self.cleaned_data.get("name", "")
        if not all(char.isalpha() or char.isspace() for char in name):
            raise ValidationError(
                "Name should contain only letters and spaces."
            )
        return name

    def save(self) -> str:
        """
        Placeholder for saving form data.

        This method can be customized to handle form submissions, such as
        saving the name to a database or sending an email.

        Returns:
        --------
        - str: The cleaned name from the form.
        """
        name: str = self.cleaned_data.get("name", "")
        # Placeholder for additional save logic
        return name


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "HelloForm",
]
