from typing import Optional, Dict, NamedTuple, List
import socket
import requests
from urllib.request import urlopen
import netifaces
import json
from ipaddress import (IPv4Network,
 IPv4Address,
 AddressValueError
)
import os
import re
from nipcat.network.types import NetworkInterface, SubnetInfo

class NetworkInfo:
    """Class providing methods to gather network information.

    This class contains static methods for retrieving various network-related
    information including external IP, internal network interfaces, and system
    hostname.
    """

    def __init__(self):
        pass

    def get_external_ip(self) -> Optional[str]:
        """Retrieves the external IP address using multiple fallback services.

        Attempts to get the external IP address using various public IP API
        services. If one service fails, it automatically tries the next one.

        Returns:
            str: The external IP address if successful.
            None: If unable to retrieve the external IP address.

        Note:
            The method tries multiple services in case some are unavailable:
            - api.ipify.org
            - api.ipapi.com
            - api.myip.com
        """
        ip_services = [
            "https://api.ipify.org?format=json",
            "https://api.ipapi.com/api/check?access_key=free",
            "https://api.myip.com"
        ]

        for service in ip_services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    return data.get('ip') or data.get('address') or data.get('query')
            except:
                continue
        return None

    def is_physical_interface(self, iface: str) -> bool:
        """Checks if a network interface is physical.

        Uses multiple methods to detect physical interfaces:
        1. Checks for virtual interface naming patterns
        2. Examines sysfs path for physical device presence
        3. Verifies interface driver information

        Args:
            iface (str): Name of the network interface

        Returns:
            bool: True if interface is physical, False otherwise
        """
        # Skip common virtual interface prefixes
        virtual_prefixes = ('veth', 'virbr', 'bridge', 'vnet', 'tun', 'tap', 'docker',
                        'vmnet', 'vboxnet', 'bond', 'team', 'dummy')
        if iface.startswith(virtual_prefixes):
            return False

        # Check sysfs paths
        sys_net_path = f"/sys/class/net/{iface}"

        # Check if interface exists in sysfs
        if not os.path.exists(sys_net_path):
            return False

        # Check for physical device
        device_link = os.path.join(sys_net_path, "device")
        if not os.path.exists(device_link):
            return False

        # Additional check for WLAN or ethernet
        uevent_path = os.path.join(sys_net_path, "uevent")
        try:
            with open(uevent_path, 'r') as f:
                uevent_content = f.read()
                if 'DEVTYPE=wlan' in uevent_content or 'DEVTYPE=ethernet' in uevent_content:
                    return True
        except (IOError, PermissionError):
            pass

        return True

    def get_interfaces(self) -> List[NetworkInterface]:
        """Retrieves information about all network interfaces.

        Gathers detailed information about each network interface including
        IP addresses, MAC addresses, netmasks, and broadcast addresses.

        Returns:
            List[NetworkInterface]: A list of NetworkInterface objects containing
                information about each network interface.

        Note:
            - Skips the loopback interface ('lo')
            - Only includes interfaces with IPv4 addresses
            - Handles errors for individual interfaces gracefully
        """
        interfaces = []

        for iface in netifaces.interfaces():
            try:
                if iface == 'lo':
                    continue
                if not self.is_physical_interface(iface):
                    continue

                addrs = netifaces.ifaddresses(iface)
                ipv4_info = addrs.get(netifaces.AF_INET, [])
                ip_addresses = [addr['addr'] for addr in ipv4_info if 'addr' in addr]

                if not ip_addresses:
                    continue

                mac_info = addrs.get(netifaces.AF_LINK, [{}])[0]
                mac_address = mac_info.get('addr')

                netmask = ipv4_info[0].get('netmask')
                broadcast = ipv4_info[0].get('broadcast')

                interface = NetworkInterface(
                    name=iface,
                    ip_addresses=ip_addresses,
                    mac_address=mac_address,
                    netmask=netmask,
                    broadcast=broadcast
                )
                interfaces.append(interface)

            except Exception:
                continue

        return interfaces

    def get_hostname(self) -> str:
        """Retrieves the system hostname.

        Returns:
            str: The hostname of the system.
        """
        return socket.gethostname()

class NetCalc:

    @staticmethod
    def is_ipv4(ip: str) -> bool:
        """Validate IP address format."""
        try:
            IPv4Address(ip)
            return True
        except AddressValueError:
            return False

    @staticmethod
    def is_private_ip(ip: IPv4Address) -> bool:
        """Check if IP address is private."""
        private_ranges = [
            IPv4Network('10.0.0.0/8'),
            IPv4Network('172.16.0.0/12'),
            IPv4Network('192.168.0.0/16')
        ]
        return any(ip in network for network in private_ranges)

    @staticmethod
    def is_valid_mask(mask:str):
        """_summary_

        Args:
            mask (str): _description_

        Returns:
            _type_: _description_
        """
        return mask.isdigit() and 0 <= int(mask) <= 32

    @staticmethod
    def is_subnet(subnet: str) -> bool:
        """_summary_

        Args:
            subnet (str): _description_

        Returns:
            bool: _description_
        """
        ip, mask = subnet.split('/')
        return NetCalc.is_ipv4(ip) and NetCalc.is_valid_mask(mask)

    @staticmethod
    def format_binary(ip: IPv4Address) -> str:
        """Convert IP to binary format with dots."""
        binary = bin(int(ip))[2:].zfill(32)
        return '.'.join(binary[i:i+8] for i in range(0, 32, 8))

    @staticmethod
    def get_network_class(ip: IPv4Address) -> str:
        """Determines the network class of an IP address.

        Args:
            ip: IPv4Address object to classify.

        Returns:
            str: Network class description (A, B, C, D, or E).
        """
        first_octet = int(str(ip).split('.')[0])
        if 1 <= first_octet <= 126:
            return "Class A"
        elif 128 <= first_octet <= 191:
            return "Class B"
        elif 192 <= first_octet <= 223:
            return "Class C"
        elif 224 <= first_octet <= 239:
            return "Class D (Multicast)"
        elif 240 <= first_octet <= 255:
            return "Class E (Reserved)"
        return "Invalid Class"

    @classmethod
    def compute(cls, subnet: str) -> SubnetInfo:
        """
        Compute all subnet information for a given subnet.

        Args:
            subnet: Subnet in CIDR notation (e.g., '192.168.1.0/24')

        Returns:
            SubnetInfo object containing all computed information

        Raises:
            ValueError: If subnet is invalid
        """
        if not cls.is_subnet(subnet):
            raise ValueError("Invalid IP address format")

        network = IPv4Network(subnet)

        network_addr = network.network_address
        broadcast_addr = network.broadcast_address
        first_host = network_addr + 1
        last_host = broadcast_addr - 1

        return SubnetInfo(
            network_address=str(network_addr),
            broadcast_address=str(broadcast_addr),
            first_host=str(first_host),
            last_host=str(last_host),
            num_hosts=network.num_addresses - 2,
            netmask=str(network.netmask),
            wildcard_mask=str(network.hostmask),
            cidr_notation=f"/{str(network.prefixlen)}",
            network_class=cls.get_network_class(network_addr),
            is_private=cls.is_private_ip(network_addr),
        )
