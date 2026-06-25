from importlib import import_module
import sys

try:
    mod = import_module("smartgrid.db.session")
    sys.modules.setdefault("app.db.session", mod)
    # Re-export commonly used symbols
    from smartgrid.db.session import engine, SessionLocal, get_db  # noqa: F401
except Exception:
    # Minimal fallback definitions
    def get_db():
        if False:
            yield
