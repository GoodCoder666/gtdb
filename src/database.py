from config import SaveMode
import os

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
        self.file.write('\n'.join(sorted(ips, key=lambda ip: tuple(map(int, ip.split('.'))))) + '\n')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
