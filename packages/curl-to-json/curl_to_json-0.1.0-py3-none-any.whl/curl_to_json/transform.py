# -*- coding: utf-8 -*-
import argparse
import base64
import json
import re
import shlex
from logging import getLogger

from six.moves import http_cookies as Cookie

logger = getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('url')
parser.add_argument('-b', '--cookie', default=[], dest='cookie', action='append')
parser.add_argument('-d', '--data', action='append', dest='data', default=[])
parser.add_argument('-X', '--request', default='GET', dest='request')
parser.add_argument('-H', '--header', action='append', default=[])
parser.add_argument('-k', '--insecure', action='store_false', default=True)
parser.add_argument('-s', '--silent', action='store_true')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-L', '--location', action='store_true', default=False)
parser.add_argument('-i', '--include', action='store_true', default=False)
parser.add_argument('-x', '--proxy', default='')
parser.add_argument('-u', '--user', default=None)
parser.add_argument('-U', '--proxy-user', default="")
parser.add_argument('-I', '--head', action='store_true', default=False)
parser.add_argument('-A', '--user-agent')
parser.add_argument('--http2', action='store_true', default=False, dest='http2')
parser.add_argument('--compressed', action='store_true')
parser.add_argument('--connect-timeout', type=int, dest='connect_timeout')
parser.add_argument('--referer', default='')


class Dict(dict):
    """
    Simple dict but support access as x.y style.
    """

    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def process_headers(headers):
    cookie_dict = dict()
    quoted_headers = dict()

    for curl_header in headers:
        if curl_header.startswith(':'):
            occurrence = [m.start() for m in re.finditer(':', curl_header)]
            header_key, header_value = curl_header[:occurrence[1]], curl_header[occurrence[1] + 1:]
        else:
            header_key, header_value = curl_header.split(":", 1)

        if header_key.lower().strip("$") == 'cookie':
            cookie = Cookie.SimpleCookie(header_value)
            for key in cookie:
                cookie_dict[key] = cookie[key].value
        else:
            quoted_headers[header_key] = header_value.strip()

    return cookie_dict, quoted_headers


def process_cookies_from_flag(cookies_lst: list):
    cookie_dict = dict()
    for cookie in cookies_lst:
        for item in cookie.split(';'):
            cookie_name, cookie_value = item.split('=', 1)
            cookie_dict[cookie_name.strip()] = cookie_value
    return cookie_dict


def process_data(headers, data):
    d = dict()
    if headers.get('Content-Type') is None:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

    if headers.get('Content-Type', '') == 'application/x-www-form-urlencoded':
        new_data = []
        for item in data:
            if '&' in item:
                new_data += item.split('&')
            else:
                new_data.append(item)
        data = new_data

        for item in data:
            key, value = item.split('=', 1)
            d[key] = value
        return headers, d

    if headers.get('Content-Type', '') == 'application/json':

        for item in data:
            try:
                data = json.loads(item)
                d.update(data)
            except ValueError as e:
                logger.warning('Invalid JSON string: {} '.format(item))

        return headers, d


def parse_context(curl_command, jsonify=False):
    request = "get"
    data = {}
    proxy = ''

    tokens = shlex.split(curl_command)
    parsed_args = parser.parse_args(tokens)

    cookie_dict, quoted_headers = process_headers(parsed_args.header)
    if parsed_args.cookie:
        cookies_from_flag = process_cookies_from_flag(parsed_args.cookie)
        cookie_dict.update(cookies_from_flag)

    # process data
    post_data = parsed_args.data
    if post_data:
        request = 'post'
        quoted_headers, data = process_data(quoted_headers, post_data)

    if parsed_args.request:
        request = parsed_args.request.lower()

    if parsed_args.head:
        request = 'head'

    if parsed_args.compressed:
        quoted_headers['Accept-Encoding'] = 'gzip, deflate'

    if parsed_args.http2:
        quoted_headers["Connection"] = "Upgrade"
        quoted_headers["Upgrade"] = "HTTP/2.0"

    if parsed_args.proxy and not parsed_args.proxy_user:
        if not parsed_args.proxy.startswith('http'):
            proxy = 'http://{}'.format(parsed_args.proxy)
        else:
            proxy = parsed_args.proxy
    if parsed_args.proxy and parsed_args.proxy_user:
        if not parsed_args.proxy.startswith('http'):
            proxy = 'http://{}@{}'.format(parsed_args.proxy_user, parsed_args.proxy)
        else:
            scheme, host = parsed_args.proxy.split('://')
            proxy = '{}://{}@{}'.format(scheme, parsed_args.proxy_user, host)

    if parsed_args.user:
        quoted_headers['Authorization'] = 'Basic {}'.format(base64.b64encode(bytes(parsed_args.user, 'utf-8')))
    if parsed_args.user_agent:
        quoted_headers['User-Agent'] = parsed_args.user_agent
    if parsed_args.referer:
        quoted_headers['Referer'] = parsed_args.referer

    dic = {
        'request': request,
        "url": parsed_args.url,
        "data": data,
        "headers": quoted_headers,
        "cookies": cookie_dict,
        "http2": parsed_args.http2,
        "location": parsed_args.location,
        "include": parsed_args.include,
        "proxy": proxy,
        'silent': parsed_args.silent,
        'verbose': parsed_args.verbose,
        'insecure': parsed_args.insecure,
        'connect_timeout': parsed_args.connect_timeout,
    }
    return json.dumps(dic) if jsonify else Dict(**dic)
