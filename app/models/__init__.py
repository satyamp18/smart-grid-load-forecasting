from importlib import import_module
import sys

try:
    mod = import_module("smartgrid.models")
    sys.modules.setdefault("app.models", mod)
    try:
        # also ensure zone submodule is available
        z = import_module("smartgrid.models.zone")
        sys.modules.setdefault("app.models.zone", z)
    except Exception:
        pass
except Exception:
    pass
