# Decentralized Exchange Platform (DEX): Proof of Concept

The decentralized exchange is an exchange platform that brings blockchain and its underlying technologies to the core functionalities of a classic exchange, which are as follows:

- Capital deposit
- Asset exchange
- Order books
- Order matching

Our goal is to design and build a cutting-edge platform that leverages multiple services among of them the exchange from fiat to cryptocurrency.

Our first implementation module is the fiat-to-crypto exchange that accepts a fiat payment and once confirmed, it triggers the desired crypto payment service and sends it to your provided wallet address. The design of the service itself ensures the safety and the atomicity of the operation.

As per the next steps, we will be working on completing the design of our solution for the remained functionalities of the decentralized exchange. The challenge is about offering a solution that is reliable, generic, immutable and does not involve a middleman. 

We have so far put in place a primary version of the first module (Fiat to crypto exchange) for the sake of demonstration. To test the application, there are two different approaches: the first one is to download the source code from our private (Github) repository (tbd) and set up the application and testing environment on your local machine. For that, please contact us to provide you the access to the repository.
The second approach is to run the application by visiting the following link                             http://gastonmg.pythonanywhere.com where the application is publicly hosted on a web server and runs as a service in the cloud. Please note that the latter implementation is still under construction. You may thus encounter some limitations while using it. We will keep maintaining this solution for you to provide you an easier and more efficient testing of our platform.

For testing purposes, a local blockchain (bitcoin) test network (regtest mode) needs to be put in place to complete the exchange cycle.
A simple testing environment is hosted with the application on the PythonAnywhere platform and offers some testing nodes that can perform transactions between each other. In case of the use of a localhost on your local machine, you can set up your own local testing network as explained in the following steps.

Setting up a local test environment:

1. Bitcoin core test network set up:

a. build the bitcoin core software: follow the steps for your preferred operating system
Install the dependencies: https://github.com/bitcoin/bitcoin/blob/master/doc/dependencies.md
Build on MacOS: https://github.com/bitcoin/bitcoin/blob/master/doc/build-osx.md
Build on Unix: https://github.com/bitcoin/bitcoin/blob/master/doc/build-unix.md
Build on Windows: https://github.com/bitcoin/bitcoin/blob/master/doc/build-windows.md

Alternatively, you can install the precompiled version of bitcoin core provided in this link https://bitcoincore.org/en/download/ please check your system requirements before installing, and make sure everything is compatible.

b. Once bitcoin core is installed on your machine you will have executables among of them “bitcoind" and “bitcoin-cli”. For testing purposes, we will set up some local test nodes (bitcoin clients) in "regtest" mode as our private bitcoin Testnet, means that they are private, local and all the data (transactions, blocks, mining etc..) are controlled by the user through the bitcoin-cli command set. You can follow this tutorial (https://www.yours.org/content/connecting-multiple-bitcoin-core-nodes-in-regtest-5fdc9c47528b) to set up some nodes on your local machine, note that in order to test transactions you will need to have at least 2 nodes and a third one as a mining node.

c. Test your nodes by trying multiple commands. For the complete list of available commands you can type the command bitcoin-cli help command. 

2. Hosting the application on your local machine

Initial setup

1.Install a custom version of Python 

[cmd] apt-get install python3==3.5.2

2.Installing Virtualenv using pip3

[cmd] pip3 install virtualenv

3.Download code source

<ul>
<li>[cmd] git clone https://github.com/TurnkeyLedger/TLDex.git</li>
<li>[cmd] cd TLDex</li>
  <li>[cmd] virtualenv env</li>
<li>[cmd] source env/bin/activate (for Linux/Mac OS ) or env\Scripts\activate.bat (for Windows)</li>
  <li>[cmd] pip3 install -r requirements.txt</li>
<li>[cmd] python manage.py migrate</li>
  <li>[cmd] python manage.py runserver</li>
</ul>

4.Open a browser and navigate to http://localhost:8000 you should see the TLdex home page

tbd

II. Access the DEX platform from the web server:

You can access the DEX platform via the link http://gastonmg.pythonanywhere.com where it is hosted. The PythonAnywhere platform is a platform as a service (PaaS) running on the cloud and serves as a public host for web applications developed with python frameworks (Django in our case). For more information please visit the website https://www.pythonanywhere.com

III. Testing the application:

1. Sign up a new account: you need to signup using and email and password

2. Login in into your already created profile

3. Execute a payment in fiat through a service payment provider (e.g Paypal) providing the bitcoin wallet address to receive the payment in crypto(bitcoin). The address must be created by one of the nodes in the local test network. For the payment module as a service, we use Paypal sandbox as a test service. You can create an account in Paypal sandbox via this link https://www.paypal.com/us/webapps/mpp/account-selection and use the created account for your payment. That will provide you a testing Paypal payment interface.

4. Starting the service: the crypto payment service is started automatically after the fiat payment is successfully completed.

5. Mining the block to confirm the transaction: the transaction is broadcast to the network and added to the “mempool" of each node in order to get mined with other available transactions. You can then mine the available transactions by generating the next block in the blockchain. The transaction is then confirmed and you will receive a confirmation notification and can also check the transaction receipt using the transaction hash. To do so, you can use the bitcoin-cli command line console to send RPC calls to the local bitcoin nodes. You can run the command bitcoin-cli help as an RPC call to have an overview of the available RPC methods. 

6. The Exchange cycle is then close. You can check the new balance of the used address and make sure it received the payment in crypto (bitcoin)


Conclusion

As per the next steps, we will work on implementing the rest of functionalities of the DEX, and include services of the top used cryptos. In a further step, we will implement a generic fully decentralized exchange service component to make the exchange operation fully decentralized and token-independent. User thus can transparently exchange against any desired crypto-token.

Please consider that the platform is still under development and yet not finalized. We are providing this 'Demo' version as a demonstration of one of the products in our portfolio in the blockchain technology. Of course, we can eventually provide the source code and share it with you on demand.

We will keep you posted!

- Turnkey Ledger team.


