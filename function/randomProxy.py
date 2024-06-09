import random

def random_proxy_choice():
    proxies = [
        "hyperion.p.shifter.io:17010",
        "hyperion.p.shifter.io:17011",
        "hyperion.p.shifter.io:17012",
        "hyperion.p.shifter.io:17013",
        "hyperion.p.shifter.io:17014"
    ]
    return random.choice(proxies)