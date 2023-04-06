import argparse
import hashlib
import requests
import threading
from queue import Queue

#example python CryptoMiner.py 12345 "transaction1" "transaction2" "transaction3" "previoushash123" "mineraddress123" BTC "cryptoaddress123" -t 4
#In this example, we are mining a block with block number 12345, containing 3 transactions: "transaction1", "transaction2", and "transaction3". The previous block's hash is "previoushash123", and we are mining for BTC currency. The miner's address is "mineraddress123", and the address to receive the mining rewards is "cryptoaddress123". We are using 4 threads to mine the block.

# Attribution information
__author__ = 'GiFXED'
__version__ = '1.3'


#PLEASE NOTE: these are just examples
MINING_POOL_URLS = {
    'BTC': 'https://mining-pool-example.com/mine_btc',
    'ETH': 'https://mining-pool-example.com/mine_eth',
    'LTC': 'https://mining-pool-example.com/mine_ltc'
}

def mine(queue, block_number, transactions, previous_hash, start_nonce, end_nonce):
    for nonce in range(start_nonce, end_nonce):
        data = str(block_number) + str(transactions) + str(previous_hash) + str(nonce)
        hash_value = hashlib.sha256(data.encode()).hexdigest()
        if hash_value.startswith('0'*6):
            print(f"Block mined with nonce value: {nonce}")
            queue.put(hash_value)
            return

def send_mined_block(queue, block_number, transactions, previous_hash, miner_address, mining_currency, crypto_address):
    while True:
        hash_value = queue.get()
        mining_pool_url = MINING_POOL_URLS[mining_currency]
        requests.post(mining_pool_url, json={'block_number': block_number, 'transactions': transactions, 'previous_hash': previous_hash, 'miner_address': miner_address, 'hash_value': hash_value, 'crypto_address': crypto_address}, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'})

def mine_blocks(num_threads, block_number, transactions, previous_hash, miner_address, mining_currency, crypto_address):
    queue = Queue()
    threads = []
    for i in range(num_threads):
        start_nonce = i * 10000000
        end_nonce = (i+1) * 10000000
        t = threading.Thread(target=mine, args=(queue, block_number, transactions, previous_hash, start_nonce, end_nonce))
        threads.append(t)
        t.start()

    t = threading.Thread(target=send_mined_block, args=(queue, block_number, transactions, previous_hash, miner_address, mining_currency, crypto_address))
    threads.append(t)
    t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crypto miner')
    parser.add_argument('block_number', type=int, help='Block number')
    parser.add_argument('transactions', nargs='+', help='List of transactions')
    parser.add_argument('previous_hash', help='Previous hash')
    parser.add_argument('miner_address', help='Miner address')
    parser.add_argument('mining_currency', choices=['BTC', 'ETH', 'LTC'], help='Currency to mine')
    parser.add_argument('crypto_address', help='Crypto address to receive rewards')
    parser.add_argument('-t', '--threads', type=int, default=8, help='Number of threads')
    args = parser.parse_args()

    mine_blocks(args.threads, args.block_number, args.transactions, args.previous_hash, args.miner_address, args.mining_currency, args.crypto_address)
