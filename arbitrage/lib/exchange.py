# coding: utf-8

import json
import time
import urllib.parse

import requests

from .helpers import (
    requestPost, httpPost, tradeLoad, requestBody, buildSign,
    signature, requestGet, httpGet
)


class exchange:
    def __init__(self, url, apiKey, secretToken, role='default'):
        """
        Role : liquidity , arbitrage , soleTrade

        """
        self.url = url
        self.apikey = apiKey
        self.secretToken = secretToken
        self.role = role

    def market(self):
        return self.role

    def buy(self, amount, price, tradePassword=None, tradeid=None):
        if self.role == 'haobtc' or self.role == 'default':
            payload = {
                'amount': amount,
                'price': price,
                'api_key': self.apikey,
                'secret_key': self.secretToken,
                'type': 'buy'
            }
            payload = tradeLoad(payload, self.secretToken, self.role)
            return requestPost(self.url['trade'], payload)

        if self.role == 'okcoin':
            params = {
                'api_key': self.apikey,
                'symbol': 'btc_cny',
                'type': 'buy'
            }

            if price:
                params['price'] = price

            if amount:
                params['amount'] = amount

            body = requestBody(self.url['trade'], self.url['host'])
            params['sign'] = buildSign(params, self.secretToken, self.role)
            r = httpPost(self.url['host'], body, params)
            if r:
                return json.loads(r)

            return None

        if self.role == 'huobi':
            params = {
                "access_key": self.apikey,
                "secret_key": self.secretToken,
                "created": int(time.time()),
                "price": price,
                "coin_type": 1,
                "amount": amount,
                "method": self.url['buy']
            }

            params['sign'] = signature(params)
            del params['secret_key']

            if tradePassword:
                params['trade_password'] = tradePassword

            if tradeid:
                params['trade_id'] = tradeid

            r = requests.post("http://" + self.url['host'], params=urllib.parse.urlencode(params))
            if r.status_code == 200:
                data = r.json()
                return data

            return None

    def bidMakerOnly(self, amount, price):
        if self.role == 'haobtc' or self.role == 'default':
            payload = {
                'amount': amount,
                'price': price,
                'api_key': self.apikey,
                'secret_key': self.secretToken,
                'type': 'buy_maker_only'
            }
            payload = tradeLoad(payload, self.secretToken, self.role)
            return requestPost(self.url['trade'], payload)

    def askMakerOnly(self, amount, price):
        if self.role == 'haobtc' or self.role == 'default':
            payload = {
                'amount': amount,
                'price': price,
                'api_key': self.apikey,
                'secret_key': self.secretToken,
                'type': 'sell_maker_only'
            }
            payload = tradeLoad(payload, self.secretToken, self.role)
            return requestPost(self.url['trade'], payload)

    def sell(self, amount, price, tradePassword=None, tradeid=None):
        if self.role == 'haobtc' or self.role == 'default':
            payload = {
                'amount': amount,
                'price': price,
                'api_key': self.apikey,
                'secret_key': self.secretToken,
                'type': 'sell'
            }
            payload = tradeLoad(payload, self.secretToken, self.role)
            return requestPost(self.url['trade'], payload)

        if self.role == 'okcoin':
            params = {
                'api_key': self.apikey,
                'symbol': 'btc_cny',
                'type': 'sell'
            }
            if price:
                params['price'] = price
            if amount:
                params['amount'] = amount

            body = requestBody(self.url['trade'], self.url['host'])
            params['sign'] = buildSign(params, self.secretToken, self.role)
            r = httpPost(self.url['host'], body, params)
            if r:
                return json.loads(r)

            return None

        if self.role == 'huobi':
            timestamp = int(time.time())
            params = {
                "access_key": self.apikey,
                "secret_key": self.secretToken,
                "created": timestamp,
                "price": price,
                "coin_type": 1,
                "amount": amount,
                "method": self.url['sell']
            }

            params['sign'] = signature(params)
            del params['secret_key']
            if tradePassword:
                params['trade_password'] = tradePassword
            if tradeid:
                params['trade_id'] = tradeid

            payload = urllib.parse.urlencode(params)
            r = requests.post("http://" + self.url['host'], params=payload)
            if r and r.status_code == 200:
                data = r.json()
                return data

            return None

    def marketBuy(self, amount):
        if self.role == 'haobtc' or self.role == 'default':
            payload = {'amount': amount, 'api_key': self.apikey, 'secret_key': self.secretToken, 'type': 'buy_market'}
            payload = tradeLoad(payload, self.secretToken, self.role)
            return requestPost(self.url['trade'], payload)

        if self.role == 'okcoin':
            body = requestBody(self.url['trade'], self.url['host'])
            params = {
                'api_key': self.apikey,
                'symbol': 'btc_cny',
                'type': 'buy_market'
            }

            if price:
                params['price'] = price

            if amount:
                params['amount'] = amount

            params['sign'] = buildSign(params, self.secretToken, self.role)
            r = httpPost(self.url['host'], body, params)
            if r:
                return json.loads(r)

            return None

        if self.role == 'huobi':
            params = {
                "access_key": self.apikey,
                "secret_key": self.secretToken,
                "created": int(time.time()),
                "coin_type": 1,
                "amount": amount,
                "method": self.url['buy_market'],
            }

            params['sign'] = signature(params)
            del params['secret_key']

            r = requests.post("http://" + self.url['host'], params=urllib.parse.urlencode(params))
            if r.status_code == 200:
                data = r.json()
                return data

            return None

    def marketSell(self, amount):
        if self.role == 'haobtc' or self.role == 'default':
            payload = {
                'amount': amount,
                'api_key': self.apikey,
                'secret_key': self.secretToken,
                'type': 'sell_market',
            }
            payload = tradeLoad(payload, self.secretToken, self.role)
            return requestPost(self.url['trade'], payload)

        if self.role == 'okcoin':
            body = requestBody(self.url['trade'], self.url['host'])
            params = {
                'api_key': self.apikey,
                'symbol': 'btc_cny',
                'type': 'buy_market'
            }

            if price:
                params['price'] = price

            if amount:
                params['amount'] = amount

            params['sign'] = buildSign(params, self.secretToken, self.role)
            r = httpPost(self.url['host'], body, params)
            if r:
                return json.loads(r)

            return None

        if self.role == 'huobi':
            params = {
                "access_key": self.apikey,
                "secret_key": self.secretToken,
                "created": int(time.time()),
                "coin_type": 1,
                "amount": amount,
                "method": self.url['sell_market'],
            }

            params['sign'] = signature(params)
            del params['secret_key']

            r = requests.post("http://" + self.url['host'], params=urllib.parse.urlencode(params))
            if r.status_code == 200:
                data = r.json()
                return data

            return None

    def cancel(self, id):
        if self.role == 'haobtc' or self.role == 'default':
            payload = {'api_key': self.apikey, "order_id": id}
            payload = tradeLoad(payload, self.secretToken, self.role)
            return requestPost(self.url['cancel_order'], payload)

        if self.role == 'okcoin':
            body = requestBody(self.url['cancel_order'], self.url['host'])
            params = {
                'api_key': self.apikey,
                'symbol': 'btc_cny',
                'order_id': id
            }

            params['sign'] = buildSign(params, self.secretToken, self.role)
            r = httpPost(self.url['host'], body, params)
            if r:
                return json.loads(r)

            return None

        if self.role == 'huobi':
            params = {
                "access_key": self.apikey,
                "secret_key": self.secretToken,
                "created": int(time.time()),
                "coin_type": 1,
                "method": self.url['cancel_order'],
                "id": id,
            }

            params['sign'] = signature(params)
            del params['secret_key']

            r = requests.post("http://" + self.url['host'], params=urllib.parse.urlencode(params))
            if r.status_code == 200:
                data = r.json()
                return data

            return None

    def cancelAll(self):
        if self.role == 'haobtc' or self.role == 'default':
            payload = {'api_key': self.apikey}
            payload = tradeLoad(payload, self.secretToken, self.role)
            return requestPost(self.url['cancel_all'], payload)

        if self.role == '':
            return

        if self.role == '':
            return

    def orderInfo(self, id):
        if self.role == 'haobtc' or self.role == 'default':
            payload = {'api_key': self.apikey, "order_id": id}
            payload = tradeLoad(payload, self.secretToken, self.role)
            return requestPost(self.url['order_info'], payload)

        if self.role == 'okcoin':
            body = requestBody(self.url['order_info'], self.url['host'])
            params = {
                'api_key': self.apikey,
                'symbol': 'btc_cny',
                'order_id': id
            }

            params['sign'] = buildSign(params, self.secretToken, self.role)
            r = httpPost(self.url['host'], body, params)
            if r:
                return json.loads(r)

            return None

        if self.role == 'huobi':
            params = {
                "access_key": self.apikey,
                "secret_key": self.secretToken,
                "created": int(time.time()),
                "coin_type": 1,
                "method": self.url['order_info'],
                "id": id,
            }

            params['sign'] = signature(params)
            del params['secret_key']

            r = requests.post("http://" + self.url['host'], params=urllib.parse.urlencode(params))
            if r.status_code == 200:
                data = r.json()
                return data

            return None

    def ordersInfo(self, id=''):
        if self.role == 'haobtc' or self.role == 'default':
            payload = {'api_key': self.apikey}
            payload = tradeLoad(payload, self.secretToken, self.role)
            return requestPost(self.url['orders_info'], payload)

        if self.role == 'okcoin':
            body = requestBody(self.url['orders_info'], self.url['host'])
            params = {
                'api_key': self.apikey,
                'symbol': 'btc_cny',
                'order_id': id,
                'type': 0
            }

            params['sign'] = buildSign(params, self.secretToken, self.role)
            r = httpPost(self.url['host'], body, params)
            if r:
                return json.loads(r)

            return None

    def orderHistory(self):
        if self.role == 'okcoin':
            body = requestBody(self.url['order_history'], self.url['host'])
            params = {
                'api_key': self.apikey,
                'current_page': 1,
                'page_length': 199,
                'status': 0,
                'symbol': 'btc_cny'
            }

            params['sign'] = buildSign(params, self.secretToken, self.role)
            r = httpPost(self.url['host'], body, params)
            if r:
                return json.loads(r)

            return None

    def historyInfo(self, size):
        if self.role == 'haobtc' or self.role == 'default':
            payload = {'api_key': self.apikey, 'size': size}
            payload = tradeLoad(payload, self.secretToken, self.role)
            return requestPost(self.url['history_info'], payload)

        if self.role == '':
            return

        if self.role == '':
            return

    def accountInfo(self):
        if self.role == 'haobtc' or self.role == 'default':
            payload = {
                'api_key': self.apikey
            }
            payload = tradeLoad(payload, self.secretToken, self.role)
            return requestPost(self.url['account_info'], payload)

        if self.role == 'okcoin':
            params = {
                'api_key': self.apikey,
            }
            body = requestBody(self.url['userInfo'], self.url['host'])
            params['sign'] = buildSign(params, self.secretToken, 'okcoin')
            r = httpPost(self.url['host'], body, params)
            if r:
                return json.loads(r)

            return None

        if self.role == 'huobi':
            params = {
                "access_key": self.apikey,
                "secret_key": self.secretToken,
                "created": int(time.time()),
                "method": self.url['account_info']
            }

            params['sign'] = signature(params)
            del params['secret_key']

            r = requests.post("http://" + self.url['host'], params=urllib.parse.urlencode(params))
            if r.status_code == 200:
                data = r.json()
                return data

            return None

    def ticker(self, symbol=''):
        if self.role == 'haobtc' or self.role == 'default':
            return requestGet(self.url['ticker'])

        if self.role == 'okcoin':
            params = ''
            body = requestBody(self.url['ticker'], self.url['host'])
            if symbol:
                params = 'symbol=%(symbol)s' % {'symbol': symbol}

            return httpGet(self.url['host'], body, params)

        if self.role == 'huobi':
            return requestGet(self.url['ticker'])

    def depth(self, size=10, merge=1, symbol=''):
        if self.role == 'haobtc' or self.role == 'default':
            payload = {
                'api_key': self.apikey,
                'size': size
            }
            payload = tradeLoad(payload, self.secretToken, self.role)
            return requestGet(self.url['depth'], payload)

        if self.role == 'okcoin':
            params = ''
            body = requestBody(self.url['depth'], self.url['host'])
            if symbol:
                params = 'symbol=%(symbol)s' % {'symbol': symbol}

            params += '&size=%(size)s&merge=%(merge)s' % {'size': size, 'merge': merge}
            return httpGet(self.url['host'], body, params)

        if self.role == 'huobi':
            # init huobi depth list to the same format as okcoin
            return {}

    def fast_ticker(self):
        if self.role == 'default' or self.role == 'haobtc':
            return requestGet(self.url['fast_ticker'])
