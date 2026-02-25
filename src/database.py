import os
from ipaddress import ip_address

from config import SaveMode

class Database:
    def __init__(self, config):
        self.mode = config.save_mode
        if not os.path.exists(config.dbfile):
            open(config.dbfile, 'w').close()
        self.file = open(config.dbfile, 'r+' if self.mode == SaveMode.APPEND else 'w')

    def save(self, ips):
        self.file.seek(0)
        if self.mode == SaveMode.APPEND:
            original_ips = self.file.read().split()
            ips = list(set(ips) | set(original_ips))
            self.file.seek(0)
        sorted_ips = sorted(ips, key=lambda x: ((ip := ip_address(x)).version, ip))
        self.file.write('\n'.join(sorted_ips) + '\n')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
