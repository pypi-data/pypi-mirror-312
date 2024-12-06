import argparse
import os
from configparser import ConfigParser

import bfqry.cli.common as c


def common() -> argparse.ArgumentParser:
    host = c.DEFAULT_HOST
    port1 = c.DEFAULT_PORT1
    port2 = c.DEFAULT_PORT2
    timeout = c.DEFAULT_TIMEOUT
    https = c.DEFAULT_HTTPS
    insecure = c.DEFAULT_INSECURE
    nocache = c.DEFAULT_NOCACHE
    for setting in c.DEFAULT_SETTINGS:
        if os.path.exists(setting):
            parser = ConfigParser()
            with open(setting) as stream:
                parser.read_string("[DEFAULT]\n" + stream.read())
            host = parser["DEFAULT"].get("batfish", c.DEFAULT_HOST)
            port1 = parser["DEFAULT"].getint("port1", c.DEFAULT_PORT1)
            port2 = parser["DEFAULT"].getint("port2", c.DEFAULT_PORT2)
            timeout = parser["DEFAULT"].getfloat("timeout", c.DEFAULT_TIMEOUT)
            https = parser["DEFAULT"].getboolean("https", c.DEFAULT_HTTPS)
            insecure = parser["DEFAULT"].getboolean("insecure", c.DEFAULT_INSECURE)
            nocache = parser["DEFAULT"].getboolean("nocache", c.DEFAULT_NOCACHE)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-b", "--base", required=True, help="Base directory.")
    parser.add_argument("--batfish", default=host, help="Batfish host address")
    parser.add_argument(
        "--port1",
        type=int,
        default=port1,
        help=f"The port batfish service is running on ({c.DEFAULT_PORT1} by default)",
    )
    parser.add_argument(
        "--port2",
        type=int,
        default=port2,
        help=f"The additional port of batfish service ({c.DEFAULT_PORT2} by default)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=timeout,
        help=f"Specifies the timeout value when connecting to Batfish. ({c.DEFAULT_TIMEOUT} by default)",
    )
    parser.add_argument(
        "--https",
        action="store_true",
        default=https,
        help="Whether to use SSL when connecting to Batfish (False by default)",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        default=insecure,
        help="Allows insecure connections",
    )
    parser.add_argument(
        "--nocache",
        action="store_true",
        default=nocache,
        help="Reuse cache.",
    )
    parser.add_argument(
        "--log",
        default="info",
        choices=["debug", "info", "warning", "error", "ciritical"],
        help="Specify the log level.",
    )
    return parser


def detail() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--detail",
        action="store_true",
        help="Detail information",
    )
    return parser


def excel() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--excel",
        default=None,
        help="Output the results in Excel",
        type=str,
    )
    return parser


def filter() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--filter",
        nargs="*",
        default=None,
        help="Only consider filters that match this specifier.",
    )
    return parser


def format() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--format",
        choices=["all", "flow", "node"],
        default="all",
        help="Specifies the output format.",
    )
    return parser


def header() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--daddr", required=True, help="Destination location/IP")
    parser.add_argument(
        "--dport", help='Destination ports as list of ranges, (e.g., "22,53-99")'
    )
    parser.add_argument("--saddr", help="Source location/IP")
    parser.add_argument(
        "--sport", help='Source ports as list of ranges (e.g., "22,53-99")'
    )
    parser.add_argument(
        "-p",
        "--protocol",
        help="List of well-known IP protocols (e.g., TCP, UDP, ICMP)",
    )
    parser.add_argument(
        "-a",
        "--application",
        help="Shorthands for application protocols (e.g., SSH, DNS, SNMP)",
    )
    parser.add_argument(
        "--icmpcodes",
        help="List of integer ICMP codes",
    )
    parser.add_argument(
        "--icmptypes",
        help="List of integer ICMP types",
    )
    parser.add_argument(
        "--dscps",
        help="List of allowed DSCP value ranges",
    )
    parser.add_argument(
        "--ecns",
        help="List of allowed ECN values ranges",
    )
    parser.add_argument(
        "--lengths",
        help="List of allowed packet length value ranges",
    )
    parser.add_argument(
        "--offsets",
        help="List of allowed fragmentOffset value ranges",
    )
    parser.add_argument(
        "--tcpflags",
        choices=[
            "ack",
            "cwr",
            "ece",
            "fin",
            "psh",
            "rst",
            "syn",
            "urg",
        ],
        help="List of MatchTcpFlags conditions on which TCP flags to match (e.g., tcpFlags, useAck, useCwr, useEce, useFin, usePsh, useRst, useSyn, useUrg)",
        nargs="*",
    )
    return parser


def node() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--node",
        help="Include nodes matching this specifier.",
        nargs="*",
    )
    return parser


def rnode() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--rnode",
        help="Include remote nodes matching this specifier.",
        nargs="*",
    )
    return parser


def start() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--node", required=True, help="Source node")
    parser.add_argument("--interface", help="Source interface")
    return parser


def summary() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Summary information",
    )
    return parser


def vrf() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--vrf",
        default=None,
        help="VRF name",
        type=str,
    )
    return parser
