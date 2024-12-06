from typing import Optional
from dataclasses import dataclass
import re

@dataclass
class NetworkInterface:
    """Data class representing a network interface.

    Attributes:
        name: The name of the network interface.
        ip_addresses: List of IP addresses associated with the interface.
        mac_address: MAC address of the interface.
        netmask: Network mask of the interface.
        broadcast: Broadcast address of the interface.
    """
    name: str
    ip_addresses: list[str]
    mac_address: Optional[str] = None
    netmask: Optional[str] = None
    broadcast: Optional[str] = None

@dataclass
class SubnetInfo:
    """
    Represents detailed information about a subnet.

    Attributes:
        network_address (str): The network address of the subnet.
        broadcast_address (str): The broadcast address of the subnet.
        first_host (str): The first usable host address in the subnet.
        last_host (str): The last usable host address in the subnet.
        num_hosts (int): The total number of usable host addresses in the subnet.
        netmask (str): The subnet mask in dot-decimal notation.
        wildcard_mask (str): The wildcard mask of the subnet.
        cidr_notation (str): The subnet in CIDR notation (e.g., "192.168.1.0/24").
        network_class (str): The class of the network (e.g., "A", "B", "C").
        is_private (bool): Whether the subnet is part of a private IP range.
    """
    network_address: str
    broadcast_address: str
    first_host: str
    last_host: str
    num_hosts: int
    netmask: str
    wildcard_mask: str
    cidr_notation: str
    network_class: str
    is_private: bool

