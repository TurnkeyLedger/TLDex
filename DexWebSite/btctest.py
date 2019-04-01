import time, requests, json

class RPCHost(object):
    def __init__(self, url):
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
                print("Couldn't connect for remote procedure call, will sleep for five seconds and then try again ({} more tries)".format(tries))
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


# Default port for the bitcoin testnet is 18332
# The port number depends on the one writtein the bitcoin.conf file
rpcPort = 3334
# The RPC username and RPC password MUST match the one in your bitcoin.conf file
rpcUser = 'rpc'
rpcPassword = 'rpc'

#Accessing the RPC local server
serverURL = 'http://' + rpcUser + ':' + rpcPassword + '@localhost:' + str(rpcPort)

#Using the class defined in the bitcoin_rpc_class.py

host = RPCHost(serverURL)
print(host.__dict__)
hash = host.call('listunspent')
print (hash)
