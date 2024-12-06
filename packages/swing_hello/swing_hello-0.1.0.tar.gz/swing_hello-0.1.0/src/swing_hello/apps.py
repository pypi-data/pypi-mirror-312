# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Provides Swing Hello Config Class
================================

This module defines the configuration class for the 'hello' application within
the Django project. It specifies various attributes and settings for the app.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library

# Import | Libraries
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# =============================================================================
# Classes
# =============================================================================

class HelloConfig(AppConfig):
    """
    Hello Config Class
    =================
    
    Configuration class for the 'hello' application.

    """

    name = "swing_hello"
    label = "swing_hello"
    verbose_name = _("Swing Hello")
    default_auto_field = "django.db.models.BigAutoField"
