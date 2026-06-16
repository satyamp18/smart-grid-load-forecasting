"""Compatibility shim package named `app`.

This file makes `import app.xxx` resolve to the existing `smartgrid.xxx`
package so code that expects the top-level package name `app` continues
to work without changing all imports in the codebase.

It's intentionally small and safe: it registers `app` modules in
sys.modules pointing to the corresponding `smartgrid` modules when
available.
"""
from __future__ import annotations

import importlib
import sys
from types import ModuleType


def _map_module(name: str) -> ModuleType | None:
    """Try to load smartgrid.<name> and register it as app.<name>.

    Returns the loaded module or None if it doesn't exist.
    """
    smart_name = f"smartgrid.{name}" if name else "smartgrid"
    try:
        module = importlib.import_module(smart_name)
    except Exception:
        return None
    sys.modules[f"app.{name}"] = module
    return module


# Do not replace the app package itself in sys.modules. Instead, lazily
# map submodules like app.core -> smartgrid.core when accessed.

# Lazily map common subpackages when accessed.
_mapped = set()


def __getattr__(name: str):
    if name in _mapped:
        return sys.modules.get(f"app.{name}")
    mod = _map_module(name)
    _mapped.add(name)
    if mod is not None:
        return mod
    raise AttributeError(f"module 'app' has no attribute '{name}'")


def __dir__():
    # Offer a minimal dir listing
    return ["api", "core", "db", "models", "schemas", "services", "tasks", "websocket"]
