"""Compatibility shim for app.db -> smartgrid.db

This module attempts to import the existing `smartgrid.db` package and
register it under the `app.db` name so code importing `app.db` works.
"""
from importlib import import_module
import sys

try:
    mod = import_module("smartgrid.db")
    sys.modules.setdefault("app.db", mod)
except Exception:
    # leave package empty if smartgrid.db not available; specific
    # submodules can be provided if needed.
    pass
