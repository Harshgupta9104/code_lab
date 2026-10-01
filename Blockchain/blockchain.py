'''
 We are going to implement the basic blockchain here 
Implement a Blockchain
    -->Header: nonce, previous_hash, timestamp, Merkle root
    -->Body: transactions
Proof of Consensus
    -->Longest valid chain
    -->Block validation
Proof of Work
    -->Find nonce for difficulty 3
    -->Hash must begin with 000...
Merkle Root
    -->alculate Merkle root from transactions

'''

# creating the basic transaction that we will use in the blockchain
'''
  First block is called the genesis block for which we decide the hash value of it 

  while other carry the previous hash of the previous hash with the calculated hash 
  '''

# importing the hashlib library that we are going to use it for the hashing in blockchain
import hashlib
import json 
import time

from matplotlib.pylab import block
# next we need the hash fuctin for hashing the transaction in the blocks of the blockchain

def calculate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# creating the fuction for calculating the merkle root\
def calculate_merkle_root(transactions):
    hashes=[]


    for transaction in transactions:
        hashes.append(calculate_hash(transaction))
        # using the while loop for recursive calculation of hashes
    while len(hashes)>1:
            new_hashes=[]

            if len(hashes)%2!=0:
                 hashes.append(hashes[-1])
            for i in range(0,len(hashes),2):
                combined_hash = hashes[i] + hashes[i+1]
                new_hash = calculate_hash(combined_hash)
                new_hashes.append(new_hash)
            hashes = new_hashes
    return hashes[0]



            
class Block :
    def __init__(self, previous_hash,index, transactions):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.index = index
        self.nonce = 0
        self.timestamp = time.time()
        self.merkle_root = calculate_merkle_root(self.transactions)
        self.hash = self.calculate_block_hash()
    def calculate_block_hash(self):
         block_header = str(self.nonce) + self.previous_hash + str(self.timestamp) + self.merkle_root
         return calculate_hash(block_header)

class Blockchain :
    def __init__(self):
         self.chain = []
         self.create_genesis_block()
         genesis_block = self.create_genesis_block()
         self.chain.append(genesis_block)
     #  creating the function for the genesis block which is the first block of the blockchain 
    def create_genesis_block(self):
        genesis_block = Block("0"*64,0,["Genesis BLock"])
        return genesis_block
    # creating the fuction for adding the next block to the chain to give it the form of the blockchain
    def add_block(self, transactions):
         previous_block = self.chain[-1]
         previous_hash = previous_block.hash
         index = previous_block.index +1
         new_block = Block(previous_hash, index, transactions)
         new_block.mine_block(3)
         self.chain.append(new_block)
    # we are creating the validation fuction if the block is valid or not by checking it 
    def is_valid_block(self,previous_block, block):
         #checking the hash if the calculated hash is same as the block hash 
         if block.hash != block.calculate_block_hash():
              return False
         # checking if the hash connecting both blocks are similar or not and it the hash is starting with 000 or not 
         if not block.hash.startswith("000"):
               return False
         if block.previous_hash != previous_block.hash:
              return False
         #checking the merkle root
         if calculate_merkle_root(block.transactions) != block.merkle_root:
              return False
         return True
    def mine_block(self, difficulty):
        target ="0"*difficulty
        while not self.hash.startswith(target):
             self.nonce = self.nonce +1
             self.hash = self.calculate_block_hash()
        