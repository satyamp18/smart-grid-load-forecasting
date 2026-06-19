from importlib import import_module
import sys

try:
    mod = import_module("smartgrid.db.base")
    # Re-export the module under app.db.base
    sys.modules.setdefault("app.db.base", mod)
    from smartgrid.db.base import Base  # noqa: F401
except Exception:
    # Minimal fallback
    class Base:  # pragma: no cover - fallback for missing imports
        pass
