import json

from dydx3 import Client
from dydx3.constants import *
from web3 import Web3


class DydxMethod:
    def __init__(self, api_file=None, web_provider_url=None):
        if api_file is None:
            api_file = 'apis.json'
        if web_provider_url is None:
            web_provider_url = 'http://localhost:8545'
        __information = json.load(open(api_file, 'r'))
        self._ETHEREUM_ADDRESS = __information['address']
        self._STARK_KEY = __information['stark_private_key']
        self._API_KEY = __information['api_key']
        self.client = Client(
                network_id=NETWORK_ID_MAINNET,
                host=API_HOST_MAINNET,
                web3=Web3(Web3.HTTPProvider(web_provider_url)),
                default_ethereum_address=self._ETHEREUM_ADDRESS,
                stark_private_key=self._STARK_KEY,
                api_key_credentials=self._API_KEY,
                )

    @staticmethod
    def a(arg):
        result = arg.data
        return result

    def authentication(self):
        user = self.a(self.get_user())
        if self._ETHEREUM_ADDRESS.lower() == str(
                user['user']['ethereumAddress']
                ):
            return 'True'
        else:
            raise ConnectionError('Authentication Failed')

    def get_free_balance(self):
        account = self.a(self.client.private.get_account())
        return float(account['account']['freeCollateral'])

    def get_position(self, market):
        account = self.a(
                self.client.private.get_positions(
                        market=market,
                        status=POSITION_STATUS_OPEN,
                        )
                )
        if not account['positions']:
            return 0
        else:
            for position in account['positions']:
                if position['market'] == market:
                    return float(position['size'])

    def get_price(self, market):
        orderbook = self.a(self.client.public.get_markets(market=market))
        return float(orderbook['markets'][market]['indexPrice'])

    def place_order(
            self, market, side, type_, size, expiration, price,
            post_only=False, limit_fee=0.005, time_in_force=None,
            trigger_price=None
            ):
        account_response = self.client.private.get_account()
        params = {
                'position_id': account_response.data['account']['positionId'],
                'market': market,  # BTC-PERP
                'side': side,  # buy or sell
                'order_type': type_,  # limit or market
                'size': str(size),
                'price': str(price),
                'post_only': post_only,
                'limit_fee': limit_fee,
                'expiration_epoch_seconds': expiration,
                }
        if trigger_price is not None:
            params['trigger_price'] = str(trigger_price)
        if time_in_force is not None:
            params['time_in_force'] = time_in_force
        order = self.a(self.client.private.create_order(**params))
        return order['order']

    def fills(self, market):
        all_fills = self.a(self.client.private.get_fills(market=market))
        return all_fills['fills']

    def get_user(self):
        return self.client.private.get_user()

    def register_api_key(self):
        api_key_response = self.client.eth_private.create_api_key()
        print(api_key_response.data)

    def get_orders(self):
        all_orders = self.client.private.get_orders(
                market=MARKET_BTC_USD,
                status=ORDER_STATUS_OPEN,
                side=ORDER_SIDE_SELL,
                # type=ORDER_TYPE_LIMIT,
                limit=50,
                )
        print(all_orders.data)