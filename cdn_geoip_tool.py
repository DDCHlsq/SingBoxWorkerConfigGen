import time

import requests
import json
import sys


def fetch_dns_records(domain):
    url = f'https://8.8.8.8/resolve?name={domain}'
    response = requests.get(url)
    data = response.json()
    return [answer['data'] for answer in data.get('Answer', []) if answer['type'] == 1]


def fetch_ip_info(ip):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    url = f'https://api.ip.sb/geoip/{ip}'
    rate_limit = 1.5
    start_time = time.time()  # 请求开始时间
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        elapsed_time = time.time() - start_time  # 计算请求耗时
        if elapsed_time < rate_limit:
            time.sleep(rate_limit - elapsed_time)  # 如果请求耗时小于请求下限，延时补足至请求下限
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"OOps: Something Else {err}")
    except json.JSONDecodeError as errj:
        print(f"JSON Decode Error: {errj} - Response Text: {response.text}")
    return None  # 返回None，表示获取信息失败


def categorize_ips_by_country(ips):
    country_ips = {}
    total_ips = len(ips)
    for i, ip in enumerate(ips):
        info = fetch_ip_info(ip)
        if info:  # 只有当info不是None时，才处理数据
            country = info.get('country')
            if country not in country_ips:
                country_ips[country] = []
            country_ips[country].append(ip)
        else:
            print(f"Failed to fetch info for IP: {ip}")
        # Update progress in the same line
        sys.stdout.write(f'\rFetching IP info: {i + 1}/{total_ips}')
        sys.stdout.flush()
    sys.stdout.write('\n')  # Move to new line after completion
    return country_ips


def main():
    domain = 'cdn-all.xn--b6gac.eu.org'
    ips = fetch_dns_records(domain)
    print(f"Found {len(ips)} IPs for domain '{domain}'.")
    country_ips = categorize_ips_by_country(ips)
    with open('ip_by_country.json', 'w') as f:
        json.dump(country_ips, f, indent=4)
    print("IPs categorized by country and saved to 'ip_by_country.json'.")


if __name__ == "__main__":
    main()
