import pytest
import sys
import os
import re
os.environ['OVERSIGHT_ENV'] = 'test'
os.environ['OVERSIGHT_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_oversight.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from coind import CoinDaemon
from ccoin_config import CoinConfig


def test_coind():
    config_text = CoinConfig.slurp_config_file(config.coin_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000002acd994a815401fbaae0e52404b32857efd0b7b0c77b8e0715ccdd6d437'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000c4e1485ee323e0dfab3c8afa871ceceff8822b9abe68005e22576d47a6f'

    creds = CoinConfig.get_rpc_creds(config_text, network)
    coind = CoinDaemon(**creds)
    assert coind.rpc_command is not None

    assert hasattr(coind, 'rpc_connection')

    # test commands without arguments
    info = coind.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert coind.rpc_command('getblockhash', 0) == genesis_hash
