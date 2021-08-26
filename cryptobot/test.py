from web3 import Web3
from web3 import Web3
from web3.middleware import geth_poa_middleware

infura_url = ""

web3 = Web3(Web3.HTTPProvider(infura_url))

add = ""

print("isConnected: ", web3.isConnected())

balance = web3.eth.getBalance(add)
print("balance ", web3.fromWei(balance, "ether"))

latest_block = web3.eth.getBlock("latest")
print("block: ", latest_block)