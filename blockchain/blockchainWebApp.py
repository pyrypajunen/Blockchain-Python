#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports
from blockchain import Blockchain
import datetime
import hashlib
import json
from flask import Flask, jsonify
from uuid import uuid4 
import requests

# Representing a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace("-", "")


# Creating A blockchain
blockchain = Blockchain()


# Mine a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    # represent get_previous_block function from blockchain class
    previous_block = blockchain.get_previous_block()
    # Take previous_block proof value from dict
    previous_proof = previous_block['proof']
    # 
    proof = blockchain.proof_of_work(previous_proof)
    # comment
    previous_hash = blockchain.hash(previous_block)
    # comment
    blockchain.add_transaction(sender = node_address,
                               receiver = "Pyry",
                               amount = "10")
    # commnet
    block = blockchain.create_block(proof, previous_hash)
    # comment
    response = {"message": 'Nice! You just mined a block',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash'],
                'transactions' : block['transactions']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    # commnet
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)}
    
    return jsonify(response), 200

# Check if block is valid
@app.route('/is_valid', methods = ['GET'])
def is_block_valid():
    
    is_valid = blockchain.is_chain_valid(chain=blockchain.chain)
    
    if is_valid:
        response = {'message' : 'All good, the blockchain is valid'}
    else:
        response = {'messege' : 'The blockchain is not valid!'}
    return jsonify(response), 200 # This tell if everyting is correct (no errors)

# Add a new transaction to the blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transactions_keys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transactions_keys):
        return "Some elements of the transactions are missing!", 400
    else:
        index = blockchain.add_transaction(json['sender'],
                                           json['receiver'],
                                           json['amount']) # return previous index
       response = {'message' : f'This transaction will be added to block {index}' }
       return jsonify(response), 201
   
# Creating new nodes
@app.route('/connect_node', methods = ['POST'])  
def connect_nodes():
    json = request.get_json()
    nodes = json.get('nodes')
    if address is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
        
    response = {"message" : " All the nodes are now connected",
                "total_nodes" : list(blockchain.nodes)}
    
    return jsonify(response), 201

@app.route('/replace_chian', methods = ['GET'])
def replace_chain():
    
    # this will tell do we have to change chain or not
    is_chain_replaced = blockchain.replace_chain()
    
    if is_chain_replaced:
        response = {'message' : 'The nodes had different chains',
                    'new_chain' : blockchain.chain}
    else:
        response = {'messege' : 'All good. The chian is the largest one.',
                    'actual_chain' : blockchain.chain}
    return jsonify(response), 200


# Running the app
app.run(host = '0.0.0.0', port = 5000)
