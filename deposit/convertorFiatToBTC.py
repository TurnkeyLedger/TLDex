import decimal

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from coinbase.wallet.client import Client

COINBASE_API_KEY = 'vnFfW3kq1R3MpC81'
COINBASE_API_SECRET = 'VdHevQp9hwmUMHtrBZdMM6cXYVkNPsmV'
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:2222"%('rpc', 'rpc'))
best_block_hash = rpc_connection.getbestblockhash()
#print(rpc_connection.getblock(best_block_hash))

"""print(rpc_connection.getnewaddress())
print(rpc_connection.listunspent())
par = {'outputs': [{'2N1ViVJJPWgN52BaAbbzQGw1LF5MVUMah76': 0.011}, {'2N4cJGCaMfT6eB7yoCrrAxE1USAgxVCPmFz': 0.0033612}],
       'inputs': [{'vout': 0, 'txid': '899c8697716b2f74c1975f3b511b87d2ac772efb877b4c3ed3777e7c3bb9a19e'},
                  {'vout': 0, 'txid': '411ba798da5bc37e74b9c1be2df92ce2047e7035851626b38f4596a396fb3f55'},
                  {'vout': 0, 'txid': 'f25ed5c7bdd6d875fa65a756a30e6244ecd6c752c09a45bd93074df5dc63339f'},
                  {'vout': 0, 'txid': 'eaf746c474a44436a3d547c033b39005f1b96ee300c39b382cde0d3377b3de4b'},
                  {'vout': 0, 'txid': 'de3bd880eb51fa75f7ca721c0f07623d68e330fab6d8c47b06ceafbb742b0c41'},
                  {'vout': 0, 'txid': '721398fd21ceff741c005875d887fce66415f53e79192cdad6599db028770223'}]}
print(rpc_connection.createrawtransaction(par))"""

from math import exp, expm1
#print(1 * 10**-8)

"""// var
dollarSatoshi = $('#oneDollarSatoshi').html();
// dollarSatoshi = addCommas(dollarSatoshi);
// $('#oneDollarSatoshi').html(dollarSatoshi);
$('#oneDollarBitcoin').html(parseFloat(parseFloat(1000 * $(
                                                              '#dollarUnit').val().replace( /\, / g, "") / oneCoinPrice * 100000).toFixed(
    0) * .00000001).toFixed(8));
$('#oneBitcoin').html(parseFloat(oneCoinPrice).toFixed(2));

print(xxxxx)"""
#print((1 *COINFRACTION) + (250000*COINFRACTION) + (20000*COINFRACTION))

# amount of bitcoins = value in USD / exchange rate
"""str_a = '5,123.000'

int_b = float(str_a.replace(',', ''))

#print("The float value", int_b)



#oneCoinPrice / 100000000 * satoshi )

_currencyCode = 'usd'

client = Client(COINBASE_API_KEY, COINBASE_API_SECRET, api_version='2.1.0')
currency_code = _currencyCode.upper()  # can also use EUR, CAD, etc.
# Make the request
sellprice = client.get_sell_price(currency_code=currency_code)

oneCoinPrice = float(sellprice.amount)

oneBTCInSatoshi = 100000000

oneSatoshiDollar = oneCoinPrice / oneBTCInSatoshi

oneDollarSatoshi = 1/oneSatoshiDollar

fiatAmount = 1

btcAmount = round(round(fiatAmount*oneDollarSatoshi,0) * 0.00000001,8)

print(oneDollarSatoshi)
print(btcAmount)
#print(btcprice)
#print(oneSatoshiDollar)
#print(oneDolarSatoshi)
#print("{:,}".format(round(oneDolarSatoshi,3)))
#print(btcamount)"""


def calculateHowMuchBitcoin(_fiatAmount,_currencyCode):
    client = Client(COINBASE_API_KEY, COINBASE_API_SECRET, api_version='2.1.0')
    currency_code = _currencyCode.upper()  # can also use EUR, CAD, etc.
    # Make the request
    sellprice = client.get_sell_price(currency_code=currency_code)
    _fiatAmountForFunc = float(_fiatAmount)
    _oneCoinPrice = float(sellprice.amount)

    _oneBTCInSatoshi = 100000000

    _oneSatoshiDollar = _oneCoinPrice / _oneBTCInSatoshi

    _oneDollarSatoshi = 1 / _oneSatoshiDollar

    btcAmount = round(round(_fiatAmountForFunc * _oneDollarSatoshi, 0) * 0.00000001, 8)

    return btcAmount

print(calculateHowMuchBitcoin('20','usd'))




































