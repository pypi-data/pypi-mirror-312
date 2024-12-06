# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Hello JSON Views Module
=======================

This module defines views that return a JSON response with a greeting message.
It includes both function-based and class-based views. The views are equipped 
with internationalization support to allow translation of messages into 
different languages.

Functions:
    - hello_json_view: A function-based view that returns a JSON response 
      with a greeting message.

Classes:
    - HelloJsonView: A class-based view that returns a JSON response 
      with a greeting message.
"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Dict

# Import | Libraries
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views import View
from django.utils.translation import gettext as _


# =============================================================================
# Function
# =============================================================================

def hello_json_view(request: HttpRequest) -> JsonResponse:
    """
    Hello JSON View Function
    ========================

    A function-based view that returns a JSON response with a greeting message.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response containing the greeting message.
    """
    data: Dict[str, str] = {"message": _("Hello, World!")}
    return JsonResponse(data)


# =============================================================================
# Classes
# =============================================================================

class HelloJsonView(View):
    """
    Hello JSON Class-Based View
    ===========================

    A class-based view that returns a JSON response with a greeting message.

    Inherits from:
        View: Django's base view class.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> JsonResponse:
        """
        Handles GET requests and returns a JSON response with a greeting
        message.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            JsonResponse: A JSON response containing the greeting message.
        """
        data: Dict[str, str] = {"message": _("Hello, World!")}
        return JsonResponse(data)


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "hello_json_view",
    "HelloJsonView",
]
