from importlib import import_module
import sys

try:
    mod = import_module("smartgrid.core.logging")
    # Re-export
    setup_logging = mod.setup_logging
except Exception:
    # Fallback minimal implementation
    import logging

    def setup_logging():
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
