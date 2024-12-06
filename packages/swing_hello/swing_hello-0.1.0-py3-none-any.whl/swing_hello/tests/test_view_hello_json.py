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

- TestHelloJsonView: Contains tests for `hello_json_view` and `HelloJsonView`.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any

# Import | Libraries
import pytest
from django.test import RequestFactory, HttpRequest
from django.http import JsonResponse
from django.utils.translation import gettext as _

# Import | Local Modules
from swing_hello.views.view_hello_json import hello_json_view, HelloJsonView


# =============================================================================
# Test Classes
# =============================================================================

@pytest.mark.django_db
class TestHelloJsonView:
    """
    Hello Views Tests Class
    =======================

    Test suite for the `hello_json_view` and `HelloJsonView` views.

    This class includes tests for GET requests to ensure that the views return 
    the correct JSON responses.
    """

    def setup_method(self) -> None:
        """
        Setup the RequestFactory for use in test methods.

        The RequestFactory is used to simulate GET requests in the test
        methods.
        """
        self.factory: RequestFactory = RequestFactory()

    def test_hello_json_view_function(self) -> None:
        """
        Test GET request handling for `hello_json_view`.

        Ensures that the function-based view returns the correct JSON
        response.
        """
        request: HttpRequest = self.factory.get("/hello/json_func")
        response: JsonResponse = hello_json_view(request)

        assert response.status_code == 200
        assert response.json() == {"message": _("Hello, World!")}

    def test_hello_json_view_class(self) -> None:
        """
        Test GET request handling for `HelloJsonView`.

        Ensures that the class-based view returns the correct JSON response.
        """
        request: HttpRequest = self.factory.get("/hello/json")
        response: JsonResponse = HelloJsonView.as_view()(request)

        assert response.status_code == 200
        assert response.json() == {"message": _("Hello, World!")}


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "TestHelloJsonView",
]
