#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Libraries in use: Flask and Postman
"""
# First blockchain implementation


### imports ###
import datetime
import hashlib
import json
from flask import Flask, jsonify



### Building a blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = [] # Represent a chain, it's is a list
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0') # Function which make a block,
        self.nodes = set()
        
    def create_block(self, proof, previous_hash): # Get previous hash come from last block of the chain
        """
        creating a block and determine block values (dict,)
        """
        block = {'index' : len(self.chain) + 1,
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash,
                 'transactions' : self.transactions}
        self.transactions = [] # updating transcation list to empty before new block is made
        self.chain.append(block)
        
        return block # Returns a new block
    
    def get_previous_block(self):
        # will give a last block of the blockchain
        return self.chain[-1]
        
    
    def proof_of_work(self, previous_proof):
        '''
        solves proof of work, when first 4 number in hash are 0000, it will return a new proof
        '''
        new_proof = 1 # set new_proof variable to 1
        check_proof = False # this stays False until the new proof is found, then is True
        while check_proof is False: # running a loop until check_proof is True
            # generates a SHA256 hash -> str format
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
        
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        """
        If previous hash of the chain is different than the new blockchain hash, Returns False (It's not valid)"""
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            # Also check previous block proof and hash operation.
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender' : sender,
            'receiver' : receiver,
            'amount' : amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

