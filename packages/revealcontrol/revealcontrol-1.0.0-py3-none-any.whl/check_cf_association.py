import ipaddress
import requests
import subprocess
import argparse

def get_cloudflare_ip_ranges():
    url = "https://www.cloudflare.com/ips-v4/"
    response = requests.get(url)
    response.raise_for_status()
    return [ipaddress.IPv4Network(ip_range) for ip_range in response.text.splitlines()]

def get_domain_ip(domain):
    result = subprocess.run(['/usr/bin/dig', domain, '+short'], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Error running dig command: {result.stderr}")
    return [ip for ip in result.stdout.strip().split('\n') if ip]

def is_ip_in_cloudflare_ranges(ip, cloudflare_ranges):
    ip_addr = ipaddress.IPv4Address(ip)
    return any(ip_addr in ip_range for ip_range in cloudflare_ranges)

def main():
    parser = argparse.ArgumentParser(description="Check if a domain is using Cloudflare.")
    parser.add_argument("domain", help="The domain name to check")
    args = parser.parse_args()

    domain = args.domain
    cloudflare_ranges = get_cloudflare_ip_ranges()
    domain_ips = get_domain_ip(domain)
    
    for ip in domain_ips:
        if is_ip_in_cloudflare_ranges(ip, cloudflare_ranges):
            print(f"The IP address {ip} is in the Cloudflare range.")
        else:
            print(f"The IP address {ip} is NOT in the Cloudflare range.")

if __name__ == "__main__":
    main()