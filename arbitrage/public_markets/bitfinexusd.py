import json
import logging
import urllib.error
import urllib.parse
import urllib.request

from .market import Market


class BitfinexUSD(Market):
    def __init__(self):
        super().__init__("USD")
        self.update_rate = 10
        self.depth = {
            'asks': [{'price': 0, 'amount': 0}],
            'bids': [{'price': 0, 'amount': 0}],
        }

    def update_depth(self):
        url = 'https://api.bitfinex.com/v1/book/btcusd'
        res = urllib.request.urlopen(url)
        jsonstr = res.read().decode('utf8')
        try:
            depth = json.loads(jsonstr)
            self.depth = self.format_depth(depth)
        except Exception:
            logging.error("%s - Can't parse json: %s" % (self.name, jsonstr))
