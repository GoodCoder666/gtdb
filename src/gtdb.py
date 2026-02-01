import asyncio

import database
from config import GtdbConfig
from scanner import IPScanner

async def monitored_scan(scanner: IPScanner, config: GtdbConfig):
    scanner_task = asyncio.create_task(scanner.start())
    await asyncio.sleep(0)

    total = sum(ip_range.num_addresses for ip_range in config.ip_ranges)
    if config.progress_bar:
        from tqdm import tqdm
        bar = tqdm(total=total)

    while scanner.running:
        scanned = scanner.scanned
        available = len(scanner.availables)
        if config.progress_bar:
            bar.n = scanned
            bar.set_postfix(available=available)
        else:
            scanned_rate, available_rate = scanned / total, (available / scanned if scanned > 0 else 0.0)
            print(f'scanned: {scanned}/{total} ({scanned_rate:.2%}), '
                  f'available: {available} ({available_rate:.2%})')
        await asyncio.sleep(config.update_interval)

    if config.progress_bar:
        bar.close()

    await scanner_task

def main():
    config = GtdbConfig('config.ini')
    scanner = IPScanner(config)

    coroutine = (scanner.start() if config.silent
                 else monitored_scan(scanner, config))
    try:
        asyncio.run(coroutine)
    except KeyboardInterrupt:
        scanner.stop()
        print('interrupted')
        if input('Save current results? (Y/n): ').lower().startswith('n'):
            return

    with database.Database(config) as db:
        db.save(scanner.availables)

    print('done')

if __name__ == '__main__':
    main()
