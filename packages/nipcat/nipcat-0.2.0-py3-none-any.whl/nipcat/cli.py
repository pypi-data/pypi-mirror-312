import click
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from ipaddress import IPv4Network
from typing import Optional
from nipcat.network import NetworkInfo, NetCalc
from nipcat.domain import DomainInfoChecker

# Theme configuration
theme = Theme({
    "property": "bold magenta",
    "value": "bright_green",
    "title": "bold cyan",
    "error": "bold red"
})
console = Console(theme=theme)

@click.command()
@click.option('-i', '--info', is_flag=True, help='Show current network information')
@click.option('-d', '--domain', is_flag=True, help='Show domain information')
@click.option('-s', '--subnet', is_flag=True, help='Show subnet information')
@click.argument('target', required=False)
def main(info: bool, domain: bool, subnet: bool, target: Optional[str]) -> None:
    """
    Network Information Processing Tool

    Provides network, domain, and subnet information based on user input.
    """
    try:
        if info:
            handle_info()
        elif domain and target:
            handle_domain(target)
        elif target:
            handle_subnet(target)
        else:
            console.print("[error]Please provide valid arguments[/error]")

    except Exception as e:
        console.print(f"[error]An error occurred: {str(e)}[/error]")

def handle_subnet(subnet: str) -> None:
    """Handle subnet calculations and display results."""
    try:
        info = NetCalc.compute(subnet)
        table = Table(
            title=f"Details for {subnet}",
            show_header=False,
            show_lines=False,
            show_edge=False
        )

        table.add_column("Property", style="property")
        table.add_column("Value", style="value")

        basic_rows = [
            ("Address", info.network_address),
            ("Netmask", info.netmask),
            ("Wildcard", info.wildcard_mask),
            ("Broadcast", info.broadcast_address),
            ("HostMin", info.first_host),
            ("HostMax", info.last_host),
            ("Hosts/Net", str(info.num_hosts)),
            ("CIDR", info.cidr_notation),
            ("Class", info.network_class),
            ("Private", "Yes" if info.is_private else "No")
        ]

        for property_name, value in basic_rows:
            table.add_row(property_name, str(value))

        console.print(table)

    except ValueError as e:
        console.print(f"[error]Invalid subnet format: {str(e)}[/error]")

def handle_info() -> None:
    """Display current network information."""
    try:
        info = NetworkInfo()
        external_ip = info.get_external_ip()
        hostname = info.get_hostname()
        interfaces = info.get_interfaces()

        table = Table(title="Network Information", show_edge=True)
        table.add_column("Property", style="property")
        table.add_column("Value", style="value")

        table.add_row("External IP", external_ip)
        table.add_row("Hostname", hostname)

        console.print(table)

        # Display interface information
        for interface in interfaces:
            interface_table = Table(
                title=f"Interface: {interface.name}",
                show_edge=True
            )
            interface_table.add_column("Property", style="property")
            interface_table.add_column("Value", style="value")

            interface_table.add_row("IP Address", interface.ip_addresses[0])
            interface_table.add_row("MAC Address", interface.mac_address)

            console.print(interface_table)

    except Exception as e:
        console.print(f"[error]Failed to retrieve network information: {str(e)}[/error]")

def handle_domain(domain: str) -> None:
    """Handle domain information retrieval and display."""
    try:
        domain_info = DomainInfoChecker(domain).get_domain_info()

        if not domain_info:
            console.print(f"[error]No information found for domain: {domain}[/error]")
            return

        table = Table(title=f"Domain Information: {domain}", show_edge=True)
        table.add_column("Property", style="property")
        table.add_column("Value", style="value")

        for key, value in domain_info.items():
            table.add_row(key, str(value))

        console.print(table)

    except Exception as e:
        console.print(f"[error]Failed to retrieve domain information: {str(e)}[/error]")

if __name__ == '__main__':
    main()
