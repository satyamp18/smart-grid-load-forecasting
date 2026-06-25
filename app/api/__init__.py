"""app.api package shim for compatibility"""

# This package contains compatibility shims that map to the project's
# `smartgrid.api` package where possible.

from importlib import import_module
import sys

try:
    sys.modules.setdefault("app.api", import_module("smartgrid.api"))
except Exception:
    # If smartgrid.api doesn't exist yet, leave the package empty; submodules
    # can still be provided directly under app.api.
    pass
