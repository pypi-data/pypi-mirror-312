"""
ReqCurl: A Python wrapper for `requests` that parses cURL commands.

Modules:
    - parser: Parses cURL commands into Python request dictionaries.
    - wrapper: Executes parsed cURL commands using `requests`.
"""

from .wrapper import reqcurl
from .parser import parse_curl

__all__ = ["reqcurl", "parse_curl"]

__version__ = "0.1.0"
