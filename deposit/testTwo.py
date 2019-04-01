import decimal
import json
import os
import random
import requests
import time
import subprocess

from coinbase.wallet.client import Client

from bitcoinrpc.authproxy import AuthServiceProxy

COINBASE_API_KEY = 'vnFfW3kq1R3MpC81'
COINBASE_API_SECRET = 'VdHevQp9hwmUMHtrBZdMM6cXYVkNPsmV'

_aliceNode = {"rpcuser": "rpc", "rpcpassword": "rpc", "rpcport": 4444, "rpcipaddress": "localhost"}
_bobNode = {"rpcuser": "rpc", "rpcpassword": "rpc", "rpcport": 6666, "rpcipaddress": "localhost"}
_networkNode = {"rpcuser": "rpc", "rpcpassword": "rpc", "rpcport": 2222, "rpcipaddress": "localhost"}

# list of all nodes
_listNodes = [_aliceNode, _bobNode, _networkNode]


class RPCHost(object):
    def __init__(self, url):
        # variable input
        self._session = requests.Session()
        self._url = url
        self._headers = {'content-type': 'application/json'}

    def call(self, rpcMethod, *params):
        payload = json.dumps({"method": rpcMethod, "params": list(params), "jsonrpc": "2.0"})
        tries = 5
        hadConnectionFailures = False
        while True:
            try:
                response = self._session.post(self._url, headers=self._headers, data=payload)
            except requests.exceptions.ConnectionError:
                tries -= 1
                if tries == 0:
                    raise Exception('Failed to connect for remote procedure call.')
                hadFailedConnections = True
                print(
                    "Couldn't connect for remote procedure call, will sleep for five seconds and then try again ({} more tries)".format(
                        tries))
                time.sleep(10)
            else:
                if hadConnectionFailures:
                    print('Connected for remote procedure call after retry.')
                break
        if not response.status_code in (200, 500):
            raise Exception('RPC connection failure: ' + str(response.status_code) + ' ' + response.reason)
        responseJSON = response.json()
        if 'error' in responseJSON and responseJSON['error'] != None:
            raise Exception('Error in RPC call: ' + str(responseJSON['error']))
        return responseJSON['result']


def selectNode(_listOfNode, _amountToSend):
    # randomlly select a node from alist
    _selectedNode = random.choice(_listOfNode)
    # dinamic variable
    _rpcUser = _selectedNode['rpcuser']
    _rpcPassword = _selectedNode['rpcpassword']
    _ipAddress = _selectedNode['rpcipaddress']
    _portNumber = _selectedNode['rpcport']
    # url to connect to
    _url = 'http://' + _rpcUser + ':' + _rpcPassword + '@' + _ipAddress + ':' + str(_portNumber)
    # function to verify balance
    _funcGetBalance = "getbalance"
    # function get list unspent
    _funcGetListUnspent = "listunspent"
    # get node balance
    _nodeBalance = RPCHost(_url).call(_funcGetBalance)
    # get node listunspent
    _nodeListUnspent = RPCHost(_url).call(_funcGetListUnspent)
    # check for balance and utxo if ok return selected node else recresif the function
    if _nodeBalance != 0.0 and _nodeBalance > _amountToSend and _nodeListUnspent != []:
        return _selectedNode
    else:
        return selectNode(_listNodes, _amountToSend)


"""
This Class run the process appove :
    1-Get All unspend UTXOs from the Wallet Node
    2-Get the most small utxo amount 
    3-From that small utxo amount we add the next small utxo to it untel we get the amount we want to send 
    4-Create a complex raw transaction that send the amount to receiver from selected utxos and the change to our address
    5-Sign the complex raw transaction (hex)
    6-Send the signed complex raw transaction to local node
    7-Check if the transaction is done
    8-Post the infos to the web server
    """


class ServiceBitcoin(object):
    def __init__(self, receiverAddress, cryptoAmountToSend):
        # A satoshi is one hundred millionth (0.00000001) of 1 coin.
        self._coinFraction = 10 ** -8
        # transaction paramateres
        self._receiverAddress = receiverAddress
        # self._fiatAmount = fiatAmount
        # self._currencyCode = currencyCode
        self._amountToSend = cryptoAmountToSend
        # dynamic variable
        # selected node to send from
        self._selectedNode = selectNode(_listNodes, self._amountToSend)
        # parameter of node
        self._rpcUser = self._selectedNode['rpcuser']
        self._rpcPassword = self._selectedNode['rpcpassword']
        self._ipAddress = self._selectedNode['rpcipaddress']
        self._portNumber = self._selectedNode['rpcport']

        # rpc host configuration
        self._rpc_connection = AuthServiceProxy(
            "http://%s:%s@%s:%d" % (self._rpcUser, self._rpcPassword, self._ipAddress, self._portNumber))
        self._session = requests.Session()
        self._rpcServerURL = 'http://' + self._rpcUser + ':' + self._rpcPassword + '@' + self._ipAddress + ':' + str(
            self._portNumber)
        # rpc header for json call
        self._headers = {'content-type': 'application/json'}
        # variable output
        # self._senderUtxos = GetUtxoWhereWeWillSpend(getUtxoInfos(),self._amountToSend).outPutUtxo().items()
        # class variable
        self._key = ""
        self._amountZero = 0.0
        self._transactionFixedFee = 20000 * self._coinFraction
        self._changeMinimumAmount = 1 * self._coinFraction
        self._changeAmountToBeBack = 0
        # rpc functions
        self._funcGetListUnspent = "listunspent"
        self._funcCreateNewAddress = "getnewaddress"
        self._funcGetPubKey = "getaddressinfo"
        self._funcCreaterawtrasaction = "createrawtransaction"
        self._funcGetPrivKey = "dumpprivkey"
        self._funcSignTransactionWithWallet = "signrawtransactionwithwallet"
        self._funcSignTransactionWithKey = "signrawtransactionwithkey"
        self._funcSendRawTransaction = "sendrawtransaction"
        self._funSetTransactionFee = "settxfee"
        self._funcEstimatedFee = "estimatesmartfee"
        self._funcGetMemoPool = "getrawmempool"
        self._funcGetNodeBalance = "getbalance"
        self._funcMineABlock = "generate"
        # rpc options
        self._dictionary = self.getUtxoInfos()

    """
    This function interact with the bitcoind server with rpc call using method and handle errors while request and response
    """

    def call(self, rpcMethod, *params):
        payload = json.dumps({"method": rpcMethod, "params": list(params), "jsonrpc": "2.0"})
        tries = 5
        hadConnectionFailures = False
        while True:
            try:
                response = self._session.post(self._rpcServerURL, headers=self._headers, data=payload)
            except requests.exceptions.ConnectionError:
                tries -= 1
                if tries == 0:
                    raise Exception('Failed to connect for remote procedure call.')
                hadFailedConnections = True
                print(
                    "Couldn't connect for remote procedure call, will sleep for five seconds and then try again ({} more tries)".format(
                        tries))
                time.sleep(10)
            else:
                if hadConnectionFailures:
                    print('Connected for remote procedure call after retry.')
                break
        if not response.status_code in (200, 500):
            raise Exception('RPC connection failure: ' + str(response.status_code) + ' ' + response.reason)
        responseJSON = response.json()
        if 'error' in responseJSON and responseJSON['error'] is not None:
            raise Exception('Error in RPC call: ' + str(responseJSON['error']))
        return responseJSON['result']

    """def calculateHowMuchBitcoin(self):
        client = Client(COINBASE_API_KEY, COINBASE_API_SECRET, api_version='2.1.0')
        currency_code = self._currencyCode.upper()  # can also use EUR, CAD, etc.
        # Make the request
        sellprice = client.get_sell_price(currency_code=currency_code)

        return float(format(float(format(self._fiatAmount, '.8f')) / float(format(float(sellprice.amount), '.8f')), '8f'))"""

    """
    1e8 is standard scientific notion, and here
    it indicates an overall scale factor for the y-axis. 
    That is, if there's a 2 on the y-axis and a 1e8 at the top, 
    the value at 2 actually indicates 2*1e8 = 2e8 = 2 * 10^8 = 200,000,000. (satoshi)
     """

    def calculateTransactionFeeAndReturnCahngeAmount(self):
        validAmount = self._amountToSend + self._transactionFixedFee + self._changeMinimumAmount

        totalSelectedUtxoAmount = self.selectedUtxos()[1]
        #print(totalSelectedUtxoAmount)

        if totalSelectedUtxoAmount > validAmount:

            self._changeAmountToBeBack = totalSelectedUtxoAmount - (self._amountToSend + self._transactionFixedFee)

        return self._changeAmountToBeBack

    # TODO get all node infos
    """def getSenderCompleteinfos(self):
        # address
        return {"sender_address": self.call(self._funcGetPubKey, self._senderAddress)['address'],
                "sender_scriptPubKey": self.call(self._funcGetPubKey, self._senderAddress)['scriptPubKey'],
                "sender_pubkey": self.call(self._funcGetPubKey, self._senderAddress)['pubkey'],
                "sender_privkey": self.call(self._funcGetPrivKey, self._senderAddress),
                }"""

    """this function create a new address to send change amount to to handel fees"""

    def createChangeAddress(self):
        return self._rpc_connection.getnewaddress()

    """this function return a dict of spendable UTXOs"""

    def getUtxoInfos(self):
        nested_dict = {}
        for v in self._rpc_connection.listunspent():
            values_dict = {'vout': v.get('vout'),
                           'amount': v.get('amount'),
                           'spendable': v.get('spendable'),
                           'scriptPubKey': v.get('scriptPubKey'),
                           'address': v.get('address')}
            # set txid a a key
            if v.get('txid') not in nested_dict.keys():
                nested_dict[v.get('txid')] = values_dict
        # return a nested dict
        return nested_dict

    """this function return the morre less spendable TXUO """

    def getMinAmountofUtxos(self):
        variable_x = list(self._dictionary.values())[0]['amount']
        for k, v in self._dictionary.items():
            if v['amount'] < variable_x:
                variable_x = v['amount']
        return variable_x

    def selectedUtxos(self):
        outputDict = {}
        if self._dictionary:
            while self._amountZero < self._amountToSend:
                for k, v in self._dictionary.items():
                    if self._dictionary[k]['amount'] == self.getMinAmountofUtxos():
                        outputDict.update({k: v})

                        self._amountZero += float(self.getMinAmountofUtxos())
                        self._key = k
                    else:
                        continue
                del self._dictionary[self._key]
        return outputDict, float(self._amountZero)

    """this function create a complex raw transaction to send from selected utxos to receiver address and 
    the change to a address that we own and return the hex of the transaction"""

    def createRawTxFromUtxo(self):
        selectedDict = self.selectedUtxos()[0]
        # print("this fee : ",self.calculateTransactionFeeAndReturnCahngeAmount())
        paramsRawTx = {"inputs":
            [

            ],
            "outputs":
                [
                    {
                        self._receiverAddress: self._amountToSend
                    },
                    {
                        # TODO check the Invalid amount error
                        str(self.createChangeAddress()): self.calculateTransactionFeeAndReturnCahngeAmount()
                    }
                ]}
        # print(selectedDict)
        if selectedDict:
            for k, v in selectedDict.items():
                # print(k)
                infos = {"txid": k, "vout": v['vout']}
                paramsRawTx['inputs'].append(infos)

            playload = json.dumps({'jsonrpc': '2.0', "method": self._funcCreaterawtrasaction, "params": paramsRawTx})
            rawTxInfo = requests.post(self._rpcServerURL, auth=(self._rpcUser, self._rpcPassword),
                                      headers=self._headers, data=playload)

            resultTx = json.loads(rawTxInfo.text)
            return resultTx.get('result')

    def signRaw(self):
        pass

    """this function sign the transaction (hex) with the wallet and return the hex of the signed transaction"""

    def signRawTxWithWallet(self):
        return self.call(self._funcSignTransactionWithWallet, self.createRawTxFromUtxo())['hex']

    """this function send the transaction to the local node and return the hex sended transaction"""

    def sendSignedRawTX(self):
        return self.call(self._funcSendRawTransaction, self.signRawTxWithWallet())

    """this function check if the transaction are validate or no and rae mined to the new block or not"""

    def checkMemoPoolForUncofrmedTx(self):
        return self.call(self._funcGetMemoPool)

    def minABlock(self):
        return self.call(self._funcMineABlock, 1)

    # TODO interact with API to see if the transaction is confirmed or not but for now we will interact with bitcoin core

    def main(self):
        print('main')
        transactinHex = self.sendSignedRawTX()
        print(transactinHex)
        time.sleep(5)
        # cmd = os.system('/home/gaston/PFE_WorK_Flow/Tools/bitcoin-0.17.1/bin/bitcoin-cli --regtest --datadir=/home/gaston/bitcoin/bob --rpcport=6666 --rpcuser=rpc --rpcpassword=rpc generate 1')
        print('im here right now ',self.minABlock())


        #print('this the process i want to run : ', self._rpc_connection.generate(1))

        time.sleep(10)
        if transactinHex not in self.checkMemoPoolForUncofrmedTx():
            return "Bitcoin payment Done"
        else:
            return "Error"


# receiverAddress = '2MvuMq6EhCd77xfmqccuEBriQ7Eo5xANJpY'
# fiatamount= 200
# currencyCode = 'usd'

# print(os.system('/home/gaston/PFE_WorK_Flow/Tools/bitcoin-0.17.1/bin/bitcoin-cli --regtest --datadir=/home/gaston/bitcoin/bob --rpcport=6666 --rpcuser=rpc --rpcpassword=rpc generate 1'))

#print("BTCprice: ", ServiceBitcoin(receiverAddress='2NF85ewEp5rQfM2kG2G6TyrEFp1sj278QDa',cryptoAmountToSend=5).main())

# print("change amount: " ,ServiceBitcoin(receiverAddress, fiatamount,currencyCode).calculateTransactionFeeAndReturnCahngeAmount())

# print("newaddress: " ,ServiceBitcoin(receiverAddress, fiatamount,currencyCode).createChangeAddress())

# print("utxounfos: " ,ServiceBitcoin(receiverAddress, fiatamount,currencyCode).getUtxoInfos())

# print("minutxo: " ,ServiceBitcoin(receiverAddress, fiatamount,currencyCode).getMinAmountofUtxos())

# print("selectedUtxos: " ,ServiceBitcoin(receiverAddress, fiatamount,currencyCode).selectedUtxos())

# print("createRawTxFromUtxo: " ,ServiceBitcoin(receiverAddress='2NDLGVGe2eYW5o4AW49fzeJkdgPSZLDhJ6E',cryptoAmountToSend=0.005014).createRawTxFromUtxo())

# print("sign: " ,ServiceBitcoin(receiverAddress, fiatamount,currencyCode).signRawTxWithWallet())
