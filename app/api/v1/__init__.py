"""app.api.v1 package shim for compatibility with smartgrid.api.v1"""

from importlib import import_module
import sys

try:
    sys.modules.setdefault("app.api.v1", import_module("smartgrid.api.v1"))
except Exception:
    pass
