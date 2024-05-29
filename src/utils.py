# -*- coding: utf-8 -*-
import ssl
import sys
from urllib.request import Request, urlopen

def _build_request(ip, host, testip_format):
    url = testip_format.format(f'[{ip}]' if ':' in ip else ip)
    request = Request(url)
    request.add_header('Host', host)
    return request

def new_context(host):
    ctx = ssl._create_unverified_context() if sys.platform.startswith('darwin') else ssl.create_default_context()
    old_wrap_socket = ctx.wrap_socket

    def new_wrap_socket(socket, **kwargs):
        kwargs['server_hostname'] = host
        return old_wrap_socket(socket, **kwargs)

    ctx.wrap_socket = new_wrap_socket
    return ctx

def check_ip(ip, timeout, host, testip_format):
    try:
        req = _build_request(ip, host, testip_format)
        urlopen(req, timeout=timeout, context=new_context(host)).close()
    except:
        return False
    return True
