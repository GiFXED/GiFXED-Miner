import hashlib
import requests
import threading
from queue import Queue

# Attribution information
__author__ = 'GiFXED'
__version__ = '1.2'

# The following code is a crypto miner created by GiFXED

block_number = 1
transactions = ['transaction1', 'transaction2']
previous_hash = '0000000000000000000000000000000000000000000000000000000000000000'

def mine(queue, block_number, transactions, previous_hash, start_nonce, end_nonce):
    for nonce in range(start_nonce, end_nonce):
        data = str(block_number) + str(transactions) + str(previous_hash) + str(nonce)
        hash_value = hashlib.sha256(data.encode()).hexdigest()
        if hash_value.startswith('0'*6):
            print(f"Block mined with nonce value: {nonce}")
            queue.put(hash_value)
            return

def send_mined_block(queue, block_number, transactions, previous_hash, miner_address):
    while True:
        hash_value = queue.get()
        requests.post('https://mining-pool.com/mine', json={'block_number': block_number, 'transactions': transactions, 'previous_hash': previous_hash, 'miner_address': miner_address, 'hash_value': hash_value}, headers={'User-Agent': 'Mozilla/5.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'})

def mine_blocks(num_threads):
    queue = Queue()
    threads = []
    for i in range(num_threads):
        start_nonce = i * 10000000
        end_nonce = (i+1) * 10000000
        t = threading.Thread(target=mine, args=(queue, block_number, transactions, previous_hash, start_nonce, end_nonce))
        threads.append(t)
        t.start()

    t = threading.Thread(target=send_mined_block, args=(queue, block_number, transactions, previous_hash, '1234567890'))
    threads.append(t)
    t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    mine_blocks(8)
