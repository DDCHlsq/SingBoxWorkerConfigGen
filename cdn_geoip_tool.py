import requests
import json

def fetch_dns_records(domain):
    url = f'https://8.8.8.8/resolve?name={domain}'
    response = requests.get(url)
    data = response.json()
    return [answer['data'] for answer in data.get('Answer', []) if answer['type'] == 1]

def fetch_ip_info(ip):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
    url = f'https://api.ip.sb/geoip/{ip}'
    response = requests.get(url, headers=headers)
    return response.json()

def categorize_ips_by_country(ips):
    country_ips = {}
    for ip in ips:
        info = fetch_ip_info(ip)
        country = info.get('country')
        if country not in country_ips:
            country_ips[country] = []
        country_ips[country].append(ip)
    return country_ips

def main():
    domain = 'cdn-all.xn--b6gac.eu.org'
    ips = fetch_dns_records(domain)
    country_ips = categorize_ips_by_country(ips)
    with open('ip_by_country.json', 'w') as f:
        json.dump(country_ips, f, indent=4)
    print("IPs categorized by country and saved to 'ip_by_country.json'.")

if __name__ == "__main__":
    main()
