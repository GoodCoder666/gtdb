# -*- coding: utf-8 -*-
import random

import aiohttp

__all__ = ['check_ip', 'get_session', 'ip_generator']

async def check_ip(session, ip, host, request_format):
    url = request_format.format(f'[{ip}]' if ':' in ip else ip)
    try:
        async with session.get(url,
                               server_hostname=host,
                               headers={'Host': host},
                               allow_redirects=False) as response:
            await response.release()
        return True
    except Exception:
        return False

def get_session(timeout):
    return aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            limit=0,
            use_dns_cache=False,
            force_close=True,
            ssl=True,
            enable_cleanup_closed=True
        ),
        timeout=aiohttp.ClientTimeout(total=timeout),
        cookie_jar=aiohttp.DummyCookieJar(),
        raise_for_status=True,
        trust_env=False,
        auto_decompress=False
    )

def ip_generator(networks, shuffle=True):
    if not shuffle:
        for net in networks:
            yield from map(str, net.hosts())
        return

    # <=512 chunks per CIDR, preferred 256 addresses per chunk
    chunks = []
    for net in networks:
        if net.num_addresses <= 256:
            chunks.append(net)
        elif net.num_addresses > 131072:
            chunks.extend(net.subnets(prefixlen_diff=9))
        else:
            chunks.extend(net.subnets(new_prefix=net.max_prefixlen - 8))

    generators = [map(str, chunk.hosts()) for chunk in chunks]
    while generators:
        random.shuffle(generators)
        next_generators = []
        for gen in generators:
            if next_ip := next(gen, None):
                yield next_ip
                next_generators.append(gen)
        generators = next_generators
