"""
This module contains custom exceptions. Consider using GenerationException in
your own code to make sure that errors are passed through to the web-app
as expected.
"""

class GenerationError(Exception):
    """
    Use this exception to create a meaningful string to be passed to
    the webapp warning panel.
    """
