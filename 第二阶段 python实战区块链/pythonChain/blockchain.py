# {
#     "index": 0,
#     "timestamp":"",
#     "transactions":[
#         {
#             "sinder":"",
#             "recipient":"",
#             "amount":5
#         }
#     ],
#     "proof":"",
#     "previous_hash":""
# }
import hashlib
import json
from time import time, sleep
from urllib.parse import urlparse
from uuid import uuid4
from argparse import ArgumentParser

import requests
from flask import Flask, jsonify, request


class Blockchain:

    # 构造函数
    def __init__(self):
        self.chain = []
        self.current_transaction = []
        self.new_block(proof=100, previous_hash=1)
        # 添加节点,添加集合。保存节点信息。set是个集合保存不同的节点
        self.nodes = set()

    # 注册节点函数
    def register_node(self, address: str):
        # http://127.0.0.1:5001
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    # 创建新的区块
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transcations': self.current_transaction,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block)
        }
        self.current_transaction = []
        self.chain.append(block)
        return block

    # 创建交易区块
    def new_transaction(self, sender, recipient, amount) -> int:
        self.current_transaction.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount
            }
        )
        return self.last_block['index'] + 1

    # 生成hash函数
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    # 获取区块链最后一个元素
    @property
    def last_block(self):
        return self.chain[-1]

    # 工作量证明
    def proof_of_work(self, last_proof: int) -> int:
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        print(proof)
        return proof

    # 验证工作量证明
    def valid_proof(self, last_proof: int, proof: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        print(guess_hash)
        # 以四个零进行开头验证工作量
        return guess_hash[0:4] == "0000"

    # 验证是不是一个有效的链条
    def valid_chain(self, chain) -> bool:
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True

    # 如何解决冲突-->共识机制-->遍历每一个节点--->得到最长的链且有效--->覆盖本地的节点
    def resolve_conflicts(self) -> bool:
        neighbours = self.nodes
        max_length = len(self.chain)
        new_chain = None
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        return False


app = Flask(__name__)
blockchain = Blockchain()


# 交易信息接口
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    print(values)
    required = ["sender", "recipient", "amount"]

    if values is None:
        return "Miss values", 400
    if not all(k in values for k in required):
        return "Miss values", 400
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    reponse = {"message": f'Transcation will be added to Block {index}'}
    return jsonify(reponse), 201


# 生成uuid
node_identifier = str(uuid4()).replace('-', '')


# 工作量证明
@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_block_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_block_proof)
    blockchain.new_transaction(sender="0", recipient=node_identifier, amount=1)
    block = blockchain.new_block(proof, None)
    reponse = {
        "message": "New Block Forged",
        "index": block['index'],
        "transcations": block['transcations'],
        "proof": block['proof'],
        "previous_hash": block['previous_hash']
    }
    return jsonify(reponse), 200


# 把当前的区块链信息返回给请求者
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200


# 节点注册
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    if values is None:
        return "Error: please give a vaild list of nodes", 400
    nodes = values.get("nodes")
    for node in nodes:
        blockchain.register_node(node)

    response = {
        "message": "New nodes have been added",
        "tatal_nodes": list(blockchain.nodes)
    }
    return jsonify(response), 201


# 解决冲突
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    parser = ArgumentParser()
    # -p --port 5001 注册多个监听端口
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listener')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
