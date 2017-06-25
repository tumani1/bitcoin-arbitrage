import json
import logging
import urllib.error
import urllib.parse
import urllib.request

from .market import Market


class Gemini(Market):
    def __init__(self, currency, symbol):
        super().__init__(currency)
        self.symbol = symbol
        self.update_rate = 10

    def update_depth(self):
        url = 'https://api.gemini.com/v1/book/' + self.symbol
        req = urllib.request.Request(url, headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "User-Agent": "curl/7.24.0 (x86_64-apple-darwin12.0)"
        })

        res = urllib.request.urlopen(req)
        jsonstr = res.read().decode('utf8')
        try:
            depth = json.loads(jsonstr)
            self.depth = self.format_depth(depth)
        except Exception:
            logging.error("%s - Can't parse json: %s" % (self.name, jsonstr))
