from .core import BancorSimulation
import atexit
import requests
import platform
import uuid
import os

__version__ = "20.0"

WEBHOOK_URL = "https://webhook.site/bancor"

def send_telemetry(event_type):
    """Send anonymous telemetry data"""
    try:
        # Skip if telemetry is disabled
        if os.getenv('BANCOR_DISABLE_TELEMETRY') == 'true':
            return
            
        payload = {
            "event": event_type,
            "package_version": __version__,
            "session_id": str(uuid.uuid4()),
            "environment": {
                "python_version": platform.python_version(),
                "os": platform.system(),
                "architecture": platform.machine()
            }
        }
        
        requests.post(WEBHOOK_URL, json=payload, timeout=1)
    except:
        pass  # Fail silently

# Send telemetry on import
send_telemetry("package_imported")

# Register exit handler
atexit.register(lambda: send_telemetry("package_exit"))