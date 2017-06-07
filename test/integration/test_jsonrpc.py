import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from coind import CoinDaemon
from ccoin_config import CoinConfig


def test_coind():
    config_text = CoinConfig.slurp_config_file(config.coin_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000183f5ea07793797e22adf61900955d5ea5ebf0d5d58d7b3240ee998ebaa'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000d141044439f376a27d3445990e4d44c752f7ae95db2a20f47dd8e09025f'

    creds = CoinConfig.get_rpc_creds(config_text, network)
    coind = CoinDaemon(**creds)
    assert coind.rpc_command is not None

    assert hasattr(coind, 'rpc_connection')

    # coind testnet block 0 hash == 00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c
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
