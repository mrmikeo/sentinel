import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from zeroone_config import ZeroOneConfig


@pytest.fixture
def zeroone_conf(**kwargs):
    defaults = {
        'rpcuser': 'zeroonerpc',
        'rpcpassword': 'AMwfPd4IF1XqmDlOKWeyX0hNpMLGi7SO0eGQcah2bml8',
        'rpcport': 29241,
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
    zeroone_config = zeroone_conf()
    creds = ZeroOneConfig.get_rpc_creds(zeroone_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'ZeroOneRPC'
    assert creds.get('password') == 'AMwfPd4IF1XqmDlOKWeyX0hNpMLGi7SO0eGQcah2bml8'
    assert creds.get('port') == 29241

    zeroone_config = zeroone_conf(rpcpassword='s00pers33kr1tzz', rpcport=8000)
    creds = ZeroOneConfig.get_rpc_creds(zeroone_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'ZeroOneRPC'
    assert creds.get('password') == 's00pers33kr1tzz'
    assert creds.get('port') == 8000

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', zeroone_conf(), re.M)
    creds = ZeroOneConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'ZeroOneRPC'
    assert creds.get('password') == 'AMwfPd4IF1XqmDlOKWeyX0hNpMLGi7SO0eGQcah2bml8'
    assert creds.get('port') == 19998


# ensure 01coin network (mainnet, testnet) matches that specified in config
# requires running zerooned on whatever port specified...
#
# This is more of a zerooned/jsonrpc test than a config test...
