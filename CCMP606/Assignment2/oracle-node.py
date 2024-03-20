# Setup
import json
import time

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from solcx import compile_source, install_solc
from web3 import Web3

# Update me: set up my Alchemy API endpoint, CoinMarketCap API key, and test account info from Metamask wallet.
alchemy_url = "" 
CMC_API = ""
my_account = ""
private_key = bytes.fromhex("")
# Deployed contract address: 0xA0608a544e61f722aee541BE90DCf483d05628AF
# Or use the following format:
# private_key = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"




# Update me: write a MyOracle contract.
MyOracleSource = "./contracts/MyOracle.sol"


def get_eth_price():
    # This function is incomplete.

    # Update me: Make sure to check out the CoinMarketCap API docs.
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest' # https://pro-api.coinmarketcap.com/ ....
    parameters = {
        'symbol': 'ETH'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        #print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    eth_in_usd = data['data']['ETH']['quote']['USD']['price']
    return eth_in_usd


def compile_contract(w3):
    # This function is complete (no updates needed) and will compile your MyOracle.sol contract.

    with open(MyOracleSource, 'r') as file:
        oracle_code = file.read()

    compiled_sol = compile_source(
        oracle_code,
        output_values=['abi', 'bin']
    )

    # Retrieve the contract interface
    contract_id, contract_interface = compiled_sol.popitem()

    # get bytecode binary and abi
    bytecode = contract_interface['bin']
    abi = contract_interface['abi']
 
    # print(w3.isAddress(w3.eth.default_account))
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    print("Compile completed!")
    return Contract 


def deploy_oracle(w3, contract):
    # This function is incomplete.

    # submit the transaction that deploys the contract
    
    deploy_txn = contract.constructor().build_transaction(
    {
        # Update me: what do you need to add to this transaction?
        'from': my_account,
        'gas': 5000000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(my_account)
    }
    )
    
    signed_txn = w3.eth.account.sign_transaction(deploy_txn, private_key=private_key)
    print("Deploying Contract......")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    # # wait for the transaction to be confirmed, and get the transaction receipt
    txn_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # # Update me: how do you retrieve the oracle address?
    oracle_address = txn_receipt.contractAddress
    return oracle_address


def update_oracle(w3, contract, ethprice):
    # This function is incomplete.
    # Convert the float value to an integer (wei)
    myprice = int(ethprice * 10**18)
    
    set_txn = contract.functions.setETHinUSD(
        myprice
    ).build_transaction({
        # Update me: what do you need to add to this transaction? 
        'to': contract.address,
        'from': my_account,
        'gas': 5000000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(my_account)
    })

    signed_txn = w3.eth.account.sign_transaction(set_txn, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # wait for the transaction to be confirmed, and get the transaction receipt
    txn_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return txn_receipt


def main():

    # install Solidity compiler and connect to Alchemy endpoint.
    install_solc('0.8.17')
    w3 = Web3(Web3.HTTPProvider(alchemy_url))
    w3.eth.default_account = my_account

    # Check if connected to endpoint
    if not w3.is_connected():
        print('Not connected to Alchemy endpoint')
        exit(-1)

    # compile and deploy contract.

    MyOracle = compile_contract(w3)
    MyOracle.address = deploy_oracle(w3, MyOracle)
    print("My oracle address:")
    print(MyOracle.address)


    # # wait for a request to the contract to update, then update the Eth price in the MyOracle contract.
    # # Update me: create an event filter from the latest block to monitor, see web3.py docs.

    event_filter = MyOracle.events.UpdatePrice.create_filter(fromBlock="latest")

    while True:
        print("Waiting for an oracle update request...")
        for event in event_filter.get_new_entries():
            # Update me: make sure the event is the correct event
            if event.event=="UpdatePrice":
                #print(event)
                print("------------------------------------------")
                print("Callback found:")
                # update oracle with data 
                # connect to coinmarketcap api to get ETH price.
                ETH_price = get_eth_price()
                print("Pulled Current ETH price:", ETH_price)
                print("Writing to blockchain...")
                txn = update_oracle(w3, MyOracle, ETH_price)
                print("Transaction complete!")
                print("blockNumber:",txn.blockNumber, "gasUsed:", txn.gasUsed)
                print("------------------------------------------")
        event_filter = MyOracle.events.UpdatePrice.create_filter(fromBlock="latest")
        # sleep 2 seconds and check the event filter again
        time.sleep(2)


if __name__ == "__main__":
    main()
