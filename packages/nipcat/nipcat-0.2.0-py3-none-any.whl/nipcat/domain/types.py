from dataclasses import dataclass, asdict, field
from typing import Optional, Any
from datetime import datetime

@dataclass
class SSLInfo:
    """
    Dataclass to represent SSL certificate information
    """
    subject: dict[str, str] = field(default_factory=dict)
    issuer: dict[str, str] = field(default_factory=dict)
    version: str = 'Unknown'
    not_before: Optional[datetime] = None
    not_after: Optional[datetime] = None
    error: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """
        Create SSLInfo instance from a dictionary
        """
        if 'error' in data:
            return cls(error=data['error'])

        try:
            return cls(
                subject=data.get('subject', {}),
                issuer=data.get('issuer', {}),
                version=data.get('version', 'Unknown'),
                not_before=cls._parse_datetime(data.get('notBefore')),
                not_after=cls._parse_datetime(data.get('notAfter'))
            )
        except Exception as e:
            return cls(error=f'Parsing error: {str(e)}')

    @staticmethod
    def _parse_datetime(date_str: Optional[str]) -> Optional[datetime]:
        """
        Parse datetime string to datetime object
        """
        if not date_str:
            return None

        try:
            return datetime.strptime(date_str, '%b %d %H:%M:%S %Y %Z')
        except ValueError:
            return None

@dataclass
class WhoisInfo:
    """
    Dataclass to represent WHOIS information
    """
    domain_name: Optional[list[str]] = field(default_factory=list)
    registrar: Optional[str] = None
    creation_date: Optional[list[datetime]] = field(default_factory=list)
    expiration_date: Optional[list[datetime]] = field(default_factory=list)
    name_servers: Optional[list[str]] = field(default_factory=list)
    emails: Optional[list[str]] = field(default_factory=list)
    status: Optional[list[str]] = field(default_factory=list)
    error: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """
        Create WhoisInfo instance from a dictionary
        """
        if 'error' in data:
            return cls(error=data['error'])

        try:
            return cls(
                domain_name=cls._convert_to_list(data.get('domain_name')),
                registrar=data.get('registrar'),
                creation_date=cls._convert_dates(data.get('creation_date', [])),
                expiration_date=cls._convert_dates(data.get('expiration_date', [])),
                name_servers=cls._convert_to_list(data.get('name_servers')),
                emails=cls._convert_to_list(data.get('emails')),
                status=cls._convert_to_list(data.get('status'))
            )
        except Exception as e:
            return cls(error=f'Parsing error: {str(e)}')

    @staticmethod
    def _convert_to_list(value: Any) -> list[str]:
        """
        Ensure value is converted to a list of strings
        """
        if value is None:
            return []
        return [value] if isinstance(value, str) else list(value)

    @staticmethod
    def _convert_dates(dates: list[Any]) -> list[datetime]:
        """
        Convert date strings or existing datetime objects to datetime
        """
        converted_dates = []
        for date in dates:
            if isinstance(date, datetime):
                converted_dates.append(date)
            elif isinstance(date, str):
                try:
                    converted_dates.append(datetime.fromisoformat(date.replace(' ', 'T')))
                except ValueError:
                    pass
        return converted_dates


@dataclass
class DNSInfo:
    """
    Comprehensive dataclass for DNS record information.

    Attributes:
        domain (str): Domain name queried.
        a_records (list[str]): IPv4 addresses.
        aaaa_records (list[str]): IPv6 addresses.
        mx_records (list[str]): Mail exchangers.
        txt_records (list[str]): Text records.
        ns_records (list[str]): Name servers.
        cname_records (list[str]): Canonical name records.
        srv_records (list[str]): Service records.
        ptr_records (list[str]): Pointer records.
        soa_records (list[str]): Start of Authority records.
        spf_records (list[str]): Sender Policy Framework records.
    """
    domain: str
    a_records: list[str] = field(default_factory=list)
    aaaa_records: list[str] = field(default_factory=list)
    mx_records: list[str] = field(default_factory=list)
    txt_records: list[str] = field(default_factory=list)
    ns_records: list[str] = field(default_factory=list)
    cname_records: list[str] = field(default_factory=list)
    srv_records: list[str] = field(default_factory=list)
    ptr_records: list[str] = field(default_factory=list)
    soa_records: list[str] = field(default_factory=list)
    spf_records: list[str] = field(default_factory=list)
