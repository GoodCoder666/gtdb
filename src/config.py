import warnings
from configparser import ConfigParser
from ipaddress import ip_network
from enum import Enum

def _check_bad(actual, expected, description):
    if not isinstance(actual, set):
        actual = set(actual)
    if not isinstance(expected, set):
        expected = set(expected)
    if unrecognized := actual - expected:
        return [f'{description}.{item}' for item in unrecognized]
    return []

def _generate_message(bad):
    if len(bad) == 1:
        return f'Unrecognized option: {bad[0]}'
    return f'Unrecognized options: {", ".join(bad)}'

class SaveMode(Enum):
    APPEND = 0
    OVERWRITE = 1

    @staticmethod
    def from_string(mode_str):
        return {'append': SaveMode.APPEND,
                'overwrite': SaveMode.OVERWRITE}[mode_str.lower()]

class GtdbConfig:
    def __init__(self, config_file, strict=False):
        config = ConfigParser()
        config.read(config_file)
        if set(config.sections()) != {'logging', 'scan', 'database'}:
            raise ValueError(
                f'Configuration Sections should be logging, scan, database; got {config.sections()}')
        logging = config['logging']
        scan = config['scan']
        database = config['database']
        bad = _check_bad(logging.keys(), {'silent', 'updateinterval', 'progressbar'}, 'logging')
        bad += _check_bad(scan.keys(), {
            'maxconnections', 'timeout', 'randomize', 'resultlimit',
            'stabilitythreshold', 'host', 'format', 'ipranges'}, 'scan')
        bad += _check_bad(database.keys(), {'dbfile', 'savemode'}, 'database')
        if bad:
            msg = _generate_message(bad)
            if strict:
                raise ValueError(msg)
            warnings.warn(msg)
        self.silent = logging.getboolean('silent', False)
        self.update_interval = logging.getfloat('updateinterval', 2.0)
        if self.update_interval <= 0:
            raise ValueError('updateInterval must be positive')
        self.progress_bar = logging.getboolean('progressbar', True)
        self.max_connections = scan.getint('maxconnections', 64)
        if self.max_connections < 1 or self.max_connections > 1024:
            raise ValueError('maxConnections must be an integer between 1 and 1024')
        self.timeout = scan.getfloat('timeout', 1.5)
        if self.timeout <= 0:
            raise ValueError('timeout must be positive')
        self.randomize = scan.getboolean('randomize', True)
        self.result_limit = scan.getint('resultlimit', 0)
        if self.result_limit < 0:
            raise ValueError('resultLimit must be non-negative')
        self.stability_threshold = scan.getint('stabilitythreshold', 3)
        if self.stability_threshold < 1 or self.stability_threshold > 100:
            raise ValueError('stabilityThreshold must be an integer between 1 and 100')
        self.host = scan.get('host', 'translate.googleapis.com')
        self.testip_format = scan.get('format', 'https://{}/translate_a/single?client=gtx&sl=en&tl=fr&q=a')
        self.ip_ranges = []
        for ip_range in scan.get('ipranges', '142.250.0.0/15').split():
            try:
                self.ip_ranges.append(ip_network(ip_range))
            except ValueError:
                raise ValueError(f'IP range "{ip_range}" is invalid')
        self.dbfile = database.get('dbfile', 'ip.txt')
        saveMode_s = database.get('savemode', 'append')
        try:
            self.save_mode = SaveMode.from_string(saveMode_s)
        except KeyError:
            raise ValueError(f'Save mode "{saveMode_s}" is invalid')
