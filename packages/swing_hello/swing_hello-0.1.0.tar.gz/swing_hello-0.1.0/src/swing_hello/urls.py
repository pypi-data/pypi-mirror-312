# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
URL Configuration
=================

Defines URL patterns for the Django application.

This module maps URLs to views, connecting web requests to the appropriate view 
logic.

The package provides the following URL patterns:

- /hello/ - Renders the template with context using HelloTemplateView.
- /hello/response - Returns a plain text “Hello!” response using HelloResponseView.
- /hello/template - Renders the template with context using HelloTemplateView.
- /hello/json - Returns a JSON response using HelloJsonView.
- /hello/json_func - Returns a JSON response using hello_json_view.
- /hello/form - Displays a form and processes form submission using HelloFormView.
- /hello/form_func - Displays a form and processes form submission using hello_form_view.
- /hello/api - A simple API endpoint returning a JSON response using HelloApiView.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
# (No standard library imports needed)

# Import | Libraries
from django.urls import path

# Import | Local Modules
from swing_hello.views.view_hello_response import HelloResponseView
from swing_hello.views.view_hello_template import HelloTemplateView


# =============================================================================
# URL Patterns
# =============================================================================

urlpatterns = [

    path(
        "",
        HelloTemplateView.as_view(),
        name = "hello"
    ),

    path(
        "response",
        HelloResponseView.as_view(),
        name = "hello_response"
    ),

    path(
        "template",
        HelloTemplateView.as_view(),
        name = "hello_template"
    ),

]



# swing_hello/urls.py

from django.urls import path
from .views import (
    HelloResponseView,
    hello_response_view,
    HelloTemplateView,
    hello_template_view,
)
from .views.view_hello_json import hello_json_view, HelloJsonView
from .views.view_hello_form import hello_form_view, HelloFormView
from .views.view_hello_api import HelloApiView

urlpatterns = [
    path('', HelloTemplateView.as_view(), name='hello'),
    path('response', HelloResponseView.as_view(), name='hello_response'),
    path('template', HelloTemplateView.as_view(), name='hello_template'),
    path('json', HelloJsonView.as_view(), name='hello_json'),
    path('json_func', hello_json_view, name='hello_json_func'),
    path('form', HelloFormView.as_view(), name='hello_form'),
    path('form_func', hello_form_view, name='hello_form_func'),
    path('api', HelloApiView.as_view(), name='hello_api'),
]