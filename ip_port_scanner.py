import socket
from concurrent.futures import ThreadPoolExecutor
import sms_config as config
def check_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            if s.connect_ex((ip, port)) == 0:
                return ip
    except Exception as e:
        return None

def scan_subnet(subnet, port):
    ips_running_port = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check_port, f"{subnet}.{i}", port) for i in range(1, 255)]
        for future in futures:
            ip = future.result()
            if ip:
                ips_running_port.append(ip)
    return ips_running_port

def get_all_running_device():
    subnet = config.SMS_SUBNET
    port = config.SMS_APP_PORT
    ips_running_port = scan_subnet(subnet, port)
    print(f"Available Gateway IP addresses:", ips_running_port)

    return ips_running_port