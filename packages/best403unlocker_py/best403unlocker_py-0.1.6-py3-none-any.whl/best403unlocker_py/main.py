import configparser
import platform
import subprocess
from typing import List
import os
from pathlib import Path

import dns.resolver
import requests
from tqdm import tqdm
import shutil
import ipaddress


def test_url_with_custom_dns(url, dns_server, results):
    def resolve_dns_with_custom_server(hostname, dns_server):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server, dns_server]
        if "://" in hostname:
            hostname = hostname.split("://")[1]
        if '/' in hostname:
            hostname = hostname.split('/')[0]
        try:
            answer = resolver.resolve(hostname)
            return answer[0].address
        except Exception as e:
            tqdm.write(f"DNS resolution error with {dns_server}: {e}")
            return None

    tqdm.write(f"Testing with DNS server: {dns_server}")
    ip_address = resolve_dns_with_custom_server(url, dns_server)
    if ip_address:
        try:
            # headers = {"Host": url}
            response = requests.get(f"http://{ip_address}", timeout=2, proxies={})
            tqdm.write(f"Status Code: {response.status_code}")
            if response.status_code >= 200 and response.status_code < 300:
                results[dns_server] = response.elapsed.total_seconds()
                tqdm.write(
                    f"*****\n\n\t\t OK {round(response.elapsed.total_seconds(),2)}\n\n*****"
                )
            # print(f"Response: {response.text}")
        except requests.RequestException as e:
            tqdm.write(f"HTTP request error: {e}")
    else:
        tqdm.write("Failed to resolve DNS.")


def get_config_path():
    home = str(Path.home())
    return os.path.join(home, '.unlock403', 'best403unlocker.conf')


def download_default_config():
    config_dir = os.path.dirname(get_config_path())
    os.makedirs(config_dir, exist_ok=True)
    try:
        response = requests.get('https://raw.githubusercontent.com/MSNP1381/best403unlocker-py/refs/heads/main/best403unlocker.conf', timeout=5)
        response.raise_for_status()
        with open(get_config_path(), 'w') as f:
            f.write(response.text)
    except requests.RequestException as e:
        tqdm.write(f"Failed to download config: {e}")
        # Provide a basic default configuration
        config = configparser.ConfigParser()
        config['dns'] = {'dns': '8.8.8.8 8.8.4.4'}
        with open(get_config_path(), 'w') as f:
            config.write(f)


def read_config():
    config_path = get_config_path()
    if not os.path.exists(config_path):
        download_default_config()
    
    config = configparser.ConfigParser()
    config.read(config_path)
    dns_servers = config.get("dns", "dns").replace('"', "").split()
    return dns_servers


def write_dns_config(dns_servers):
    config = configparser.ConfigParser()
    config["dns"] = {"dns": " ".join(dns_servers)}
    with open(get_config_path(), "w") as configfile:
        config.write(configfile)


def sort_dict(results: dict):
    values = sorted(results.items(), key=lambda item: item[1])
    return [i[0] for i in values]


def set_dns(dns_servers: List[str]):
    os_type = platform.system().lower()

    def validate_dns_servers(dns_servers):
        valid_dns_servers = []
        for i in dns_servers:
            try:
                ipaddress.ip_address(i)
                valid_dns_servers.append(i)
            except ValueError:
                tqdm.write(f"Invalid DNS server IP: {i}")
                exit()
        return valid_dns_servers

    dns_servers = validate_dns_servers(dns_servers)
    if os_type == "windows":
        set_dns_windows(dns_servers)
    elif os_type == "darwin":
        set_dns_mac(dns_servers)
    elif os_type == "linux":
        set_dns_linux(dns_servers)
    else:
        print(f"Unsupported OS: {os_type}")


def set_dns_windows(dns_servers):
    # ***The requested operation requires elevation (Run as administrator).***
    # interface = "Ethernet"  # Change this to your network interface name if different
    # command = f'netsh interface ip set dns name="{interface}" static {dns_servers[0]}'
    # subprocess.run(command, shell=True)
    # for dns in dns_servers[1:]:
    #     command = f'netsh interface ip add dns name="{interface}" {dns} index=2'
    #     subprocess.run(command, shell=True)
    # Beautiful print with "*" padding and Windows logo in ASCII
    columns, _ = shutil.get_terminal_size()
    padding = "*" * columns

    windows_logo = """
             _.-;;-._
      '-..-'|   ||   |
      '-..-'|_.-;;-._|
      '-..-'|   ||   |
jgs   '-..-'|_.-''-._|"""
    print(padding)
    print(windows_logo)
    print("Windows detected")
    print("windows doesn't support changing DNS servers, change it manually")
    print()
    print(padding)
    print(dns_servers[0])
    if len(dns_servers) > 1:
        print(dns_servers[1])
    print()

    print(padding)
    print()


def set_dns_mac(dns_servers):
    network_service = "Wi-Fi"  # Change this to your network service name if different
    dns_string = ",".join(dns_servers)
    command = f"networksetup -setdnsservers {network_service} {dns_string}"
    subprocess.run(command, shell=True)


def set_dns_linux(dns_servers):
    resolv_conf = "/etc/resolv.conf"
    with open(resolv_conf, "w") as file:
        for dns in dns_servers:
            file.write(f"nameserver {dns}\n")


def scan_dns_servers(url, dns_servers):
    results = {i: 1000 for i in dns_servers}
    for dns_server in tqdm(dns_servers, desc="Testing DNS servers"):
        test_url_with_custom_dns(url, dns_server, results)
    return results


def main():
    url = "developers.google.com"
    dns_servers = read_config()
    results = scan_dns_servers(url, dns_servers)
    sorted_dns_servers = sort_dict(results)
    write_dns_config(sorted_dns_servers)
    set_dns(sorted_dns_servers)


if __name__ == "__main__":
    main()
