import shlex
from typing import List, Union

HEARTBEAT_STR = "HEARTBEAT_INTERVAL="
OPTIONS_STR = "OPTIONS="
PORT_STR = "PORT="


class LicenseParser:
    def __init__(self, path):
        self.license_file = None
        self.path = path
        self.server: Union[Server, None] = None
        self.vendor: Union[Vendor, None] = None
        self.use_server = False
        self.features: List[Feature] = []

    def __enter__(self):
        self.open()
        return self

    def open(self):
        self.license_file = open(self.path)
        self._parse()
        return self

    def _parse(self):
        i = 2
        lines = [line.strip() for line in self.license_file if line.strip()]
        self.server = Server(lines[0])
        self.vendor = Vendor(lines[1])
        if lines[2] == "USE_SERVER":
            self.use_server = True
            i += 1

        while i < len(lines):
            comment = None
            if lines[i][0] == '#':
                comment = lines[i]
                i += 1
            ft = Feature(comment, lines[i])
            self.features.append(ft)
            i += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return self

    def close(self):
        self.license_file.close()

    def __str__(self):
        return f"Server:      {self.server}\n" \
               f"Vendor:      {self.vendor}\n" \
               f"Use_server:  {self.use_server}\n" \
               f"Features:    {[str(x) for x in self.features]}"


class Server:
    host = None
    host_id = None
    port = None
    primary_is_master = False
    heartbeat = None

    def __init__(self, server):
        ssplit = server.split(' ')
        if ssplit[0] != "SERVER":
            raise RuntimeError(f"Server line expected to start with \"SERVER\": instead got: {ssplit[0]}")
        self.host = ssplit[1]
        self.host_id = ssplit[2]
        for field in ssplit[3:]:
            if field == "PRIMARY_IS_MASTER":
                self.primary_is_master = True
            elif field.startswith(HEARTBEAT_STR):
                self.heartbeat = field[len(HEARTBEAT_STR):]
            else:
                self.port = field

    def __str__(self):
        return f"host: {self.host}, host_id: {self.host_id}"


class Vendor:
    vendor = None
    daemon_path = None
    options = None
    port = None

    def __init__(self, vendor):
        vsplit = vendor.split(" ")
        if vsplit[0] != "VENDOR":
            raise RuntimeError(f"Vendor line must start with \"VENDOR\", instead got: {vendor}")

        self.vendor = vsplit[1]

        for field in vsplit[2:]:
            if field.startswith(OPTIONS_STR):
                self.options = field[len(OPTIONS_STR):]
            elif field.startswith(PORT_STR):
                self.port = field[len(PORT_STR):]
            else:
                self.daemon_path = field


class Feature:
    comment = None
    expires = None
    feature = None
    vendor = None
    version = None
    exp_date = None
    license_count = None
    opt_fields = {}

    def __init__(self, comment, feat):
        if comment:
            self.comment = comment.lstrip("#").strip()

        isplit = shlex.split(feat)
        self.feature = isplit[1]
        self.vendor = isplit[2]
        self.version = isplit[3]
        self.exp_date = isplit[4]  # Consider date parsing
        self.license_count = isplit[5]
        for field in isplit[6:-1]:
            fsplit = field.split("=")
            if len(fsplit) > 1:
                self.opt_fields[fsplit[0]] = fsplit[1]
            else:
                self.opt_fields[fsplit[0]] = True
        self.sign = isplit[-1].lstrip("SIGN=").lstrip("AUTH=")

    def __str__(self):
        return f"Product: {self.comment}, Expires: {self.expires}"
