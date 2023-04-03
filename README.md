# Crypto Miner

This is a simple crypto mining script created by GiFXED. It uses the SHA256 hashing algorithm to mine blocks and sends them to a mining pool website.

## Usage

To use this script, you will need to have Python 3 installed on your machine. You can download Python 3 from the official website [here](https://www.python.org/downloads/).

To get started with the script, follow these steps:

1. Clone this repository to your local machine using Git or download the zip file and extract it.
2. Navigate to the directory where the `crypto_miner.py` file is located.
3. Install the required dependencies by running the following command in your terminal:

pip install -r requirements.txt

4. Modify the `block_number`, `transactions`, `previous_hash`, and `miner_address` variables in the `CryptoMiner.py` file to suit your needs.
5. Run the script using the following command:

python CryptoMiner.py

The script will automatically divide the mining workload among multiple threads for maximum efficiency.

## Customization

You can customize the following variables in the `CryptoMiner.py` file:

- `block_number`: The block number of the block being mined.
- `transactions`: A list of transactions included in the block.
- `previous_hash`: The hash of the previous block in the blockchain.
- `miner_address`: The address of the mining pool to which mined blocks will be sent.

You can also modify the `mine` function to use a different hashing algorithm or adjust the difficulty of the mining process.

## Disclaimer

This script is for educational purposes only and should not be used for illegal activities. The creator of this script is not responsible for any damages or losses caused by the use of this script.
