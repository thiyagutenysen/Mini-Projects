import socket


def get_local_ip_address(target):
    ipaddr = ''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((target, 8000))
        ipaddr = s.getsockname()[0]
        s.close()
    except:
        pass

    return ipaddr


print("Raspberry Pi - Local IP Address")
print(get_local_ip_address('10.0.1.1'))
print(get_local_ip_address('google.com'))
