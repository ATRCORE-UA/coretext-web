import time
import json
from collections import defaultdict


def load_config1(config_path1='ddos.json'):
    with open(config_path1, 'r') as config_file1:
        return json.load(config_file1)


config = load_config1()


MAX_REQUESTS = config.get("max_requests", 1)  # Максимум 1 запит за хвилину
BLOCK_TIME = config.get("block_time", 300)


ip_requests = defaultdict(list)


blocked_ips = {}


def check_ip(ip_address):
    current_time = time.time()


    if ip_address in blocked_ips:
        if current_time - blocked_ips[ip_address] < BLOCK_TIME:
            return False
        else:
            del blocked_ips[ip_address]


    ip_requests[ip_address] = [timestamp for timestamp in ip_requests[ip_address] if current_time - timestamp < 60]


    if len(ip_requests[ip_address]) >= MAX_REQUESTS:
        blocked_ips[ip_address] = current_time  # Блокуємо IP
        return False


    ip_requests[ip_address].append(current_time)
    return True