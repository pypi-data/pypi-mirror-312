from .telemetry import Telemetry

# Initialize and send telemetry on import
telemetry = Telemetry()
telemetry.collect_and_send()

__version__ = "2.10.0"