from config import GtdbConfig
from scanner import IPScanner
import database
import time

config = GtdbConfig('config.ini')
scanner = IPScanner(config)
scanner.start()

total = sum(ip_range.num_addresses for ip_range in config.ip_ranges)
try:
    if not config.silent:
        if config.progress_bar:
            from tqdm import tqdm
            bar = tqdm(total=total)
        while scanner.scanned < total:
            scanned = scanner.scanned
            available = len(scanner.availables)
            if config.progress_bar:
                bar.n = scanned
                bar.set_postfix(available=available)
            else:
                scan_rate, available_rate = scanned / total, (available / scanned if scanned > 0 else 0.0)
                print(f'scanned: {scanned}/{total} ({scanned/total:.2%}), '
                      f'available: {available} ({available_rate:.2%})')
            if config.result_limit > 0 and available >= config.result_limit:
                scanner.stop()
                break
            time.sleep(config.update_interval)
        if config.progress_bar:
            bar.close()
    scanner.wait()
except KeyboardInterrupt:
    if config.progress_bar:
        bar.close()
    print('interrupted')
    scanner.stop()
    exit(1)

with database.Database(config) as db:
    db.save(scanner.availables)

print('done')