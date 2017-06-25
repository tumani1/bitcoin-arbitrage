# Copyright (C) 2016, Philsong <songbohr@gmail.com>

import lib.broker_api as exchange_api
from .market import Market


class BrokerCNY(Market):
    def __init__(self):
        super().__init__('CNY')
        self.update_rate = 1
        exchange_api.init_broker()

    def update_depth(self):
        depth = {}
        try:
            ticker = exchange_api.exchange_get_ticker()
            depth['asks'] = [[ticker.ask, 30]]
            depth['bids'] = [[ticker.bid, 30]]
        except Exception as e:
            exchange_api.init_broker()
            return

        self.depth = self.format_depth(depth)
