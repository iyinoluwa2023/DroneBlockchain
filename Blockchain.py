from hashlib import sha256
import json


class Block:
    def __init__(self, index, data, previous_hash):
        """
        :param index: Unique Block ID
        :param data: Tuple of latitude and longitude coordinates
        :param previous_hash: Hash of the previous block
        """
        self.index = index
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = None
        self.hash = None

    def compute_hash(self):
        """
        Creates and returns hash of block object
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:
    # Difficulty of proof of work function
    difficulty = 2

    def __init__(self):
        """
        Constructor for the `Blockchain` class.
        """
        self.chain = []
        self.create_genesis_block()
        self.unconfirmed_data = []

    def create_genesis_block(self):
        """
        Constructor of the initial block in the chain with and index
        of 0, no positional data, and a previous hash of 0
        """
        genesis_block = Block(0, (), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        """
        Returns the most recent block in the chain.
        """
        return self.chain[-1]

    @staticmethod
    def proof_of_work(block):
        """
        Function that uses brute force to trie different values of the
        nonce to get a valid hash value for a block
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        # The greater the value of Blockchain.difficulty, the more time will be needed for a solution to be determined
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        # Returns valid hash
        return computed_hash

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification.
        Verification includes:
        * Checking if the proof is valid.
        * The previous_hash referred in the block and the hash of a latest block
          in the chain match.
        """
        # Saves hash of the last block
        previous_hash = self.last_block.hash

        # Add block operation fails if proof not valid or the previous hash is not correct
        if previous_hash != block.previous_hash:
            return False
        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    @staticmethod
    def is_valid_proof(block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def add_new_data(self, data):
        self.unconfirmed_data.append(data)

    def mine(self):
        """
        Converts all un-mined transcations into a block object, verifies their hash
        and then adds them to the chain
        """
        if not self.unconfirmed_data:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          data=self.unconfirmed_data,
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_data = []
        return new_block.index


