# foop/__init__.py
from .telemetry import Telemetry

# Initialize telemetry when package is imported
telemetry = Telemetry()

__version__ = "60.0.0"