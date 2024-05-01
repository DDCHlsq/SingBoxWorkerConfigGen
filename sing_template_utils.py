# sing-box config template JSON
template_json = {
    "log": {
        "disabled": False,
        "level": "info",
        "timestamp": True
    },
    "dns": {
        "servers": [
            {
                "tag": "cf",
                "address": "https://1.1.1.1/dns-query",
                "strategy": "prefer_ipv4",
                "detour": "proxy"
            },
            {
                "tag": "cftls",
                "address": "tls://1.1.1.1",
                "strategy": "ipv4_only",
                "detour": "proxy"
            },
            {
                "tag": "googletls",
                "address": "tls://8.8.8.8",
                "strategy": "prefer_ipv4",
                "detour": "proxy"
            },
            {
                "tag": "google",
                "address": "https://8.8.8.8/dns-query",
                "strategy": "prefer_ipv4",
                "detour": "proxy"
            },
            {
                "tag": "ali",
                "address": "https://223.5.5.5/dns-query",
                "strategy": "prefer_ipv4",
                "detour": "direct"
            },
            {
                "tag": "dnspod",
                "address": "https://1.12.12.12/dns-query",
                "strategy": "prefer_ipv4",
                "detour": "direct"
            },
            {
                "tag": "dnspodtls",
                "address": "tls://1.12.12.12",
                "strategy": "prefer_ipv4",
                "detour": "direct"
            }
        ],
        "rules": [
            {
                "outbound": "any",
                "server": "ali"
            },
            {
                "rule_set": "rule-direct",
                "server": "ali"
            },
            {
                "rule_set": "rule-private",
                "server": "ali"
            },
            {
                "rule_set": "rule-icloud",
                "server": "ali"
            },
            {
                "rule_set": "rule-apple",
                "server": "ali"
            }
        ],
        "final": "google",
        "disable_cache": False,
        "disable_expire": False,
        "independent_cache": False,
        "reverse_mapping": False,
        "fakeip": {
            "enabled": False
        }
    },
    "inbounds": [
    ],
    "outbounds": [
        {
            "type": "selector",
            "tag": "proxy",
            "outbounds": [
            ],
            "default": "CM1",
            "interrupt_exist_connections": False
        },
        {
            "type": "dns",
            "tag": "dns-out"
        },
        {
            "tag": "direct",
            "type": "direct",
            "domain_strategy": "prefer_ipv4"
        },
        {
            "type": "block",
            "tag": "block"
        }
    ],
    "route": {
        "rules": [
            {
                "protocol": "dns",
                "outbound": "dns-out"
            },
            {
                "domain": [
                    "yyhnet.top",
                    "ddch.one"
                ],
                "domain_suffix": [
                    ".yyhnet.top",
                    ".ddch.one"
                ],
                "outbound": "direct"
            },
            {
                "rule_set": "rule-private",
                "outbound": "direct"
            },
            {
                "rule_set": "rule-reject",
                "outbound": "block"
            },
            {
                "rule_set": "rule-icloud",
                "outbound": "direct"
            },
            {
                "rule_set": "rule-apple",
                "outbound": "direct"
            },
            {
                "rule_set": "geosite-cn",
                "outbound": "direct"
            },
            {
                "rule_set": "rule-proxy",
                "outbound": "proxy"
            },
            {
                "rule_set": "rule-tld-not-cn",
                "outbound": "proxy"
            },
            {
                "rule_set": "rule-direct",
                "outbound": "direct"
            },
            {
                "rule_set": "rule-telegramcidr",
                "outbound": "proxy"
            },
            {
                "rule_set": "rule-cncidr",
                "outbound": "direct"
            },
            {
                "ip_is_private": True,
                "outbound": "direct"
            }
        ],
        "rule_set": [
            {
                "tag": "geosite-cn",
                "type": "remote",
                "format": "binary",
                "url": "https://raw.githubusercontent.com/SagerNet/sing-geosite/rule-set/geosite-cn.srs",
                "download_detour": "proxy"
            },
            {
                "tag": "rule-direct",
                "type": "remote",
                "format": "binary",
                "url": "https://raw.githubusercontent.com/DDCHlsq/sing-ruleset/ruleset/direct.srs",
                "download_detour": "proxy"
            },
            {
                "tag": "rule-proxy",
                "type": "remote",
                "format": "binary",
                "url": "https://raw.githubusercontent.com/DDCHlsq/sing-ruleset/ruleset/proxy.srs",
                "download_detour": "proxy"
            },
            {
                "tag": "rule-reject",
                "type": "remote",
                "format": "binary",
                "url": "https://raw.githubusercontent.com/DDCHlsq/sing-ruleset/ruleset/reject.srs",
                "download_detour": "proxy"
            },
            {
                "tag": "rule-private",
                "type": "remote",
                "format": "binary",
                "url": "https://raw.githubusercontent.com/DDCHlsq/sing-ruleset/ruleset/private.srs",
                "download_detour": "proxy"
            },
            {
                "tag": "rule-apple",
                "type": "remote",
                "format": "binary",
                "url": "https://raw.githubusercontent.com/DDCHlsq/sing-ruleset/ruleset/apple.srs",
                "download_detour": "proxy"
            },
            {
                "tag": "rule-icloud",
                "type": "remote",
                "format": "binary",
                "url": "https://raw.githubusercontent.com/DDCHlsq/sing-ruleset/ruleset/icloud.srs",
                "download_detour": "proxy"
            },
            {
                "tag": "rule-tld-not-cn",
                "type": "remote",
                "format": "binary",
                "url": "https://raw.githubusercontent.com/DDCHlsq/sing-ruleset/ruleset/tld-not-cn.srs",
                "download_detour": "proxy"
            },
            {
                "tag": "rule-telegramcidr",
                "type": "remote",
                "format": "binary",
                "url": "https://raw.githubusercontent.com/DDCHlsq/sing-ruleset/ruleset/telegramcidr.srs",
                "download_detour": "proxy"
            },
            {
                "tag": "rule-cncidr",
                "type": "remote",
                "format": "binary",
                "url": "https://raw.githubusercontent.com/DDCHlsq/sing-ruleset/ruleset/cncidr.srs",
                "download_detour": "proxy"
            }
        ],
        "final": "proxy",
        "auto_detect_interface": True
    },
    "experimental": {
        "cache_file": {
            "enabled": True
        }
    }
}

mobile_inbounds = [{
    "tag": "tun",
    "type": "tun",
    "inet4_address": "172.19.0.1/30",
    "inet6_address": "fdfe:dcba:9876::1/126",
    "mtu": 1400,
    "stack": "system",
    "auto_route": True,
    "strict_route": True,
    "sniff": True,
    "sniff_override_destination": True
}]

desktop_inbounds = [
    {
        "tag": "mixed7890",
        "type": "mixed",
        "listen": "127.0.0.1",
        "listen_port": 7890,
        "sniff": True
    },
    {
        "tag": "mixed7891",
        "type": "mixed",
        "listen": "127.0.0.1",
        "listen_port": 7891,
        "sniff": True
    }
]
