from dataclasses import dataclass, asdict, field
import re
import socket
import ssl
import whois
from .types import SSLInfo, WhoisInfo, DNSInfo
from typing import Any, Optional
import dns.resolver

class DomainInfoChecker:
    def __init__(self, domain):
        """
        Initialize the DomainInfoChecker with input validation methods.
        """
        self.domain = domain

    def validate_domain(self) -> bool:
        """
        Validate the domain name format.

        Args:
            domain (str): Domain name to validate

        Returns:
            bool: True if domain is valid, False otherwise
        """
        # Regular expression for domain validation
        domain_pattern = re.compile(
            r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$',
            re.IGNORECASE
        )

        if not isinstance(self.domain, str):
            return False

        # Remove protocol and trailing path if present
        domain = self.domain.lower().replace('http://', '').replace('https://', '').split('/')[0]

        return bool(domain_pattern.match(domain))

    def get_ssl_info(self, domain: str) -> SSLInfo:
        """
        Retrieve SSL certificate information for a domain.

        Args:
            domain (str): Domain to check SSL certificate

        Returns:
            SSLInfo with certificate details or error information
        """
        if not self.validate_domain(self.domain):
            raise ValueError(f"Invalid domain: {domain}")

        try:
            # Attempt to create an SSL context and retrieve certificate
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as secure_sock:
                    cert = secure_sock.getpeercert()

                    ssl_dict = {
                        'subject': dict(x[0] for x in cert['subject']),
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'version': cert.get('version', 'Unknown'),
                        'notBefore': cert.get('notBefore'),
                        'notAfter': cert.get('notAfter')
                    }

                    return SSLInfo.from_dict(ssl_dict)
        except (socket.error, ssl.SSLError) as e:
            return SSLInfo(error=f'SSL retrieval failed: {str(e)}')

    def get_whois_info(self, domain: str) -> WhoisInfo:
        """
        Retrieve WHOIS information for a domain.

        Args:
            domain (str): Domain to retrieve WHOIS information

        Returns:
            WhoisInfo with domain registration details
        """
        if not self.validate_domain(self.domain):
            raise ValueError(f"Invalid domain: {self.domain}")

        try:
            # Retrieve WHOIS information
            domain_whois = whois.whois(self.domain)

            # Convert whois object to dictionary
            whois_dict = {k: v for k, v in domain_whois.items() if v is not None}

            return WhoisInfo.from_dict(whois_dict)

        except Exception as e:
            return WhoisInfo(error=f'WHOIS retrieval failed: {str(e)}')

    def get_dns_info(self) -> Optional[DNSInfo]:
        """
        Retrieve comprehensive DNS records for a domain.

        Args:
            domain (str): Domain to query.

        Returns:
            Optional[DNSInfo]: DNS record information or None on failure.
        """
        record_types = {
            'A': 'a_records',
            'AAAA': 'aaaa_records',
            'MX': 'mx_records',
            'TXT': 'txt_records',
            'NS': 'ns_records',
            'CNAME': 'cname_records',
            'SRV': 'srv_records',
            'PTR': 'ptr_records',
            'SOA': 'soa_records',
            'SPF': 'spf_records'
        }

        try:
            dns_info = DNSInfo()

            for record_type, attr_name in record_types.items():
                try:
                    records = dns.resolver.resolve(self.domain, record_type)

                    if record_type == 'MX':
                        setattr(dns_info, attr_name, [str(rdata.exchange) for rdata in records])
                    elif record_type == 'SOA':
                        setattr(dns_info, attr_name, [str(records[0])])
                    else:
                        setattr(dns_info, attr_name, [str(rdata) for rdata in records])
                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                    continue
                except Exception as e:
                    print(f"Error retrieving {record_type} records: {e}")

            return dns_info

        except Exception as e:
            print(f"Unexpected DNS retrieval error: {e}")
            return None

    def get_domain_info(self) -> dict[str, Any]:
        """
        Comprehensive method to get both SSL and WHOIS information.

        Args:
            domain (str): Domain to retrieve information for

        Returns:
            Dict containing SSL and WHOIS information
        """
        if not self.validate_domain(self.domain):
            raise ValueError(f"Invalid domain: {self.domain}")

        return {
            'ssl_info': asdict(self.get_ssl_info(self.domain)),
            'whois_info': asdict(self.get_whois_info(self.domain)),
            'dns_info': asdict(self.get_dns_info(self.domain))
        }
