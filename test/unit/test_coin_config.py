import pytest
import os
import sys
import re
os.environ['OVERSIGHT_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_oversight.conf'))
os.environ['OVERSIGHT_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from ccoin_config import CoinConfig


@pytest.fixture
def coin_conf(**kwargs):
    defaults = {
        'rpcuser': 'OVSD',
        'rpcpassword': 'OVSD7oJSQUHt',
        'rpcport': 29683,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    coind_config = coin_conf()
    creds = CoinConfig.get_rpc_creds(coind_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'OVSD'
    assert creds.get('password') == 'OVSD7oJSQUHt'
    assert creds.get('port') == 28683

    coind_config = coin_conf(rpcpassword='OVSD7oJSQUHt', rpcport=28683)
    creds = CoinConfig.get_rpc_creds(coind_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'OVSD'
    assert creds.get('password') == 'OVSD7oJSQUHt'
    assert creds.get('port') == 28683

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', coin_conf(), re.M)
    creds = CoinConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'OVSD'
    assert creds.get('password') == 'OVSD7oJSQUHt'
    assert creds.get('port') == 28683

# This is more of a coind/jsonrpc test than a config test...
