# -*- coding: UTF-8 -*-
import socket

# addr = ("www.xicidaili.com", 80)
# addr = ("183.148.135.226", 9999)
addr = ("223.241.116.154", 8010)

host = "223.241.116.154"
port = 8010


def is_connection_up(address, timeout=1):
    _s = None
    try:
        _s = socket.create_connection(address=address, timeout=timeout)
    except socket.timeout:
        pass
    finally:
        _s.close() if _s else None
    return _s


# conn = http.client.HTTPConnection("183.148.135.226", 9999)
# conn.set_tunnel("www.xicidaili.com")
# conn.request("GET", "/nn")
# r = conn.getresponse()
# print(r.status)

print(is_connection_up(addr))
