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
                api_key_credentials=self._API_KEY
                )

    def get_user(self):
        user = self.client.private.get_user()
        print(user.data)

    def register_api_key(self):
        api_key_response = self.client.eth_private.create_api_key()
        print(api_key_response.data)
