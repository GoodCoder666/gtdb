from concurrent.futures import ThreadPoolExecutor
import utils
import random

class IPScanner:
    def __init__(self, config):
        self.config = config
        self.availables = []
        self.scanned = 0
        self.executor = ThreadPoolExecutor(max_workers=self.config.num_threads)

    def _scan_ip(self, ip):
        for _ in range(self.config.stability_threshold):
            if not utils.check_ip(ip, self.config.timeout, self.config.host, self.config.testip_format):
                self.scanned += 1
                return
        self.availables.append(ip)
        self.scanned += 1

    def start(self):
        ip_lists = []
        for ip_list in map(list, self.config.ip_ranges):
            if self.config.randomize:
                random.shuffle(ip_list)
            ip_lists.append(ip_list)
        while ip_lists:
            new_ip_lists = []
            for ip_list in ip_lists:
                self.executor.submit(self._scan_ip, str(ip_list.pop()))
                if ip_list:
                    new_ip_lists.append(ip_list)
            ip_lists = new_ip_lists

    def wait(self):
        self.executor.shutdown()

    def stop(self):
        self.executor.shutdown(cancel_futures=True)