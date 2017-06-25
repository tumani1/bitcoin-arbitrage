import json
import logging
import urllib.error
import urllib.parse
import urllib.request

from .market import Market


class Kraken(Market):
    def __init__(self, currency, code):
        super().__init__(currency)
        self.code = code
        self.update_rate = 10

    def update_depth(self):
        url = 'https://api.kraken.com/0/public/Depth'
        req = urllib.request.Request(url, b"pair=" + bytes(self.code, "ascii"),
                                     headers={
                                         "Content-Type": "application/x-www-form-urlencoded",
                                         "Accept": "*/*",
                                         "User-Agent": "curl/7.24.0 (x86_64-apple-darwin12.0)"})
        res = urllib.request.urlopen(req)
        jsonstr = res.read().decode('utf8')
        try:
            depth = json.loads(jsonstr)
            self.depth = self.format_depth(depth['result'][self.code])
        except Exception:
            logging.error("%s - Can't parse json: %s" % (self.name, jsonstr))
