import os
from importlib import import_module

try:
    mod = import_module("smartgrid.core.config")
    settings = mod.settings
except Exception:
    # Minimal fallback Settings-like object
    class _Fallback:
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
        REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    settings = _Fallback()
