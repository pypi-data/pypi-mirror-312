import hashlib
import os

import requests
from pybatfish.client.session import Session

import bfqry.cli.common as c


def debug_line() -> None:
    c.logger.debug(f"{c.SEPARATOR1}")


def debug(*message: str) -> None:
    for _ in message:
        c.logger.debug(_)


def info_line() -> None:
    c.logger.info(f"{c.SEPARATOR1}")


def info(*message: str) -> None:
    for _ in message:
        c.logger.info(_)


def error(*message: str) -> None:
    for _ in message:
        c.logger.error(_)


class BaseException(Exception):
    def __init__(self, arg=""):
        self.arg = arg


class TimeoutError(BaseException):
    def __str__(self):
        return f"Could not connect to Batfish.: {self.arg}"


class ConnectionError(BaseException):
    def __str__(self):
        return f"Connection refused.: {self.arg}"


class Batfish:
    def __init__(
        self,
        host=c.DEFAULT_HOST,
        base=c.DEFAULT_BASE,
        port1=c.DEFAULT_PORT1,
        port2=c.DEFAULT_PORT2,
        https=c.DEFAULT_HTTPS,
        insecure=c.DEFAULT_INSECURE,
        timeout=c.DEFAULT_TIMEOUT,
        nocache=c.DEFAULT_NOCACHE,
    ):
        self.host = host
        self.base = base
        self.port1 = port1
        self.port2 = port2
        self.https = https
        self.insecure = insecure
        self.timeout = timeout
        self.nocache = nocache

    def get_session(self) -> Session:
        # Check connection to Batfish.
        url = f"http{'s' if self.https else ''}://{self.host}:{self.port2}/"
        try:
            requests.get(
                url=url,
                timeout=float(self.timeout),
            )
        except requests.exceptions.Timeout:
            raise TimeoutError(url)
        except requests.exceptions.ConnectionError:
            raise ConnectionError(url)

        # Initialize the connection.
        bf = Session(
            host=self.host,
            port_v1=self.port1,
            port_v2=self.port2,
            ssl=self.https,
            verify_ssl_certs=self.insecure,
        )
        tmpname = hashlib.sha1(self.base.replace("/", "-").encode("utf-8")).hexdigest()
        snapshot_path = self.base
        snapshot_name = tmpname + "_snapshot"
        network = tmpname + "_network"
        hash = snapshot_path + "/hash"
        bf.set_network(network)

        # Check the cache.
        if self.nocache:
            self.write_hash(hash, self.base)
            bf.init_snapshot(snapshot_path, name=snapshot_name, overwrite=True)
        elif not os.path.exists(hash):
            self.write_hash(hash, self.base)
            bf.init_snapshot(snapshot_path, name=snapshot_name, overwrite=True)
        else:
            hash1 = self.read_hash(hash)
            hash2 = self.calc_hash(self.base)
            if hash1 == hash2:
                try:
                    bf.init_snapshot(snapshot_path, name=snapshot_name, overwrite=False)
                except:
                    bf.set_snapshot(name=snapshot_name)
            else:
                self.write_hash(hash, self.base)
                bf.init_snapshot(snapshot_path, name=snapshot_name, overwrite=True)
        return bf

    def calc_hash(self, path: str) -> str:
        hash = hashlib.sha1()
        hash = self.hash_dirs(path, c.HASH_DIRS, hash)
        hash = self.hash_files(path, c.HASH_FILES, hash)
        return hash.hexdigest()

    def hash_dirs(self, path: str, targets: list, hash: hashlib.sha1) -> hashlib.sha1:
        for target in targets:
            base = os.path.join(path, target)
            if os.path.isdir(base):
                hash = self.hash_files(base, os.listdir(base), hash)
        return hash

    def hash_files(self, base: str, targets: list, hash: hashlib.sha1) -> hashlib.sha1:
        for target in targets:
            if os.path.isfile(base + "/" + target):
                with open(base + "/" + target, "rb") as f:
                    while True:
                        buf = f.read(hash.block_size * 0x800)
                        if not buf:
                            break
                        hash.update(buf)
        return hash

    def read_hash(self, file: str) -> str:
        with open(file) as f:
            return f.read()

    def write_hash(self, file: str, path: str):
        with open(file, mode="w") as f:
            f.write(self.calc_hash(path))
