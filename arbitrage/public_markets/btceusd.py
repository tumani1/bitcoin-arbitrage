import json
import urllib.error
import urllib.parse
import urllib.request

from .market import Market


class BtceUSD(Market):
    def __init__(self):
        super(BtceUSD, self).__init__("USD")
        self.update_rate = 10

    def update_depth(self):
        url = 'https://btc-e.com/api/2/btc_usd/depth'
        req = urllib.request.Request(url, None, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "User-Agent": "curl/7.24.0 (x86_64-apple-darwin12.0)"
        })
        res = urllib.request.urlopen(req)
        depth = json.loads(res.read().decode('utf8'))
        self.depth = self.format_depth(depth)


if __name__ == "__main__":
    market = BtceUSD()
    print(market.get_ticker())
