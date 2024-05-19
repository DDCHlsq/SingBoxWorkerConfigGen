import requests
import json
import sys
import sing_template_utils

def main(domain, uuid, platform, path):
    template_json = sing_template_utils.template_json
    mobile_inbounds = sing_template_utils.mobile_inbounds
    desktop_inbounds = sing_template_utils.desktop_inbounds

    # Step 1: Retrieve IP list from the API
    url = 'https://api.hostmonit.com/get_optimization_ip'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({"key": "iDetkOys"})
    response = requests.post(url, headers=headers, data=data)
    ip_list = response.json()

    # Step 2: Filter and sort IPs
    valid_ips = ip_list['info']
    sorted_ips = sorted(valid_ips, key=lambda x: x['line'])

    # Step 3: Organize IPs by line and add to the template JSON
    line_counters = {'CM': 1, 'CU': 1, 'CT': 1}
    for ip in sorted_ips:
        line = ip['line']
        colo = ip['colo']
        new_tag = f"{line}{line_counters[line]}-{colo}" if colo.lower() != "default" else f"{line}{line_counters[line]}"
        new_node = {
            "type": "vless",
            "tag": new_tag,
            "server": ip['ip'],
            "server_port": 2052,
            "uuid": uuid,
            "tls": {
                "enabled": False
            },
            "transport": {
                "type": "ws",
                "path": path,
                "headers": {
                    "Host": domain
                },
                "early_data_header_name": "Sec-WebSocket-Protocol",
                "max_early_data": 2048
            }
        }
        template_json['outbounds'].append(new_node)
        template_json['outbounds'][0]['outbounds'].append(new_tag)
        line_counters[line] += 1

    # Set the default outbound to the first new node added
    template_json['outbounds'][0]['default'] = template_json['outbounds'][0]['outbounds'][0]

    if platform == "mobile":
        template_json['inbounds'] = mobile_inbounds
    elif platform == "desktop":
        template_json['inbounds'] = desktop_inbounds
    else:
        raise ValueError("Unsupported platform specified")

    # Save the modified template JSON to a file
    with open(f"sing_cf_{platform}.json", 'w') as f:
        json.dump(template_json, f, indent=2)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python main.py <domain> <uuid> <platform> <path>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
