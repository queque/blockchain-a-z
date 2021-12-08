# importar las librerias
import datetime
import hashlib
import json

import flask
from flask import Flask, jsonify


# parte 1 - crear la cadena de bloques
class Blockchain:

    # Constructor de python
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    #  Resolvemos la ecuación, la codificamos y la devolvemos cifrada en SHA256
    #  El problema matemático que debe resolver no ha de ser simétrico; Con polinomios suele ser suficiente
    #  Hacer pruebas cambiando la fórmula para ver la dificultad al minar
    def get_cypher_hash(self, previous_proof, current_proof):
        ecuation = current_proof ** 2 - previous_proof ** 2
        encoded_ecuation = str(ecuation).encode()
        return hashlib.sha256(encoded_ecuation).hexdigest()

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,  # Guardamos la posición del nuevo bloque
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = self.get_cypher_hash(new_proof, previous_proof)
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    # Debemos ordenar para que el diccionario siempre esté en el mismo orden. Ya que si es "random"
    # al codificar dará un hash distinto, haciendo que falle por efecto de avalancha
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    # Iteramos sobre nuestra cadena con las siguientes validaciones:
    #   - si los hashes de las cadenas no son iguales, la invalidamos en el momento
    #   - si el hash no empieza por 0000, invalidamos la cadena en el momento
    # Si recorremos toda la cadena sin que ninguna de estas validaciones salte, es que la cadena es correcta
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            current_block = chain[block_index]
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            hash_operation = self.get_cypher_hash(current_block['proof'], previous_block['proof'])
            if hash_operation[:4] != '0000':
                return False
            previous_block = current_block
            block_index += 1
        return True


# Parte 2 - minado de un bloque de la cadena
# crear una aplicación web
app = Flask(__name__)
# Si se obtiene un error 500. actualizar Flask, reiniciar Pycharm
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# crear una Bloackchain
blockchain = Blockchain()


# http://127.0.0.1:5000/
# Minar un nuevo Bloque
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': '¡Enhorabuena! has minado un nuevo bloque',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


# Bienvenida al server
@app.route('/', methods=['GET'])
def hello():
    response = '<h1>Bienvenido al servidor Flask de Blockchain A-Z</h1>'
    return response, 200


# TAREA 1: Reto Final
# Comprobamos si la cadena es válida
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid_chain = blockchain.is_chain_valid(blockchain.chain)
    message = 'Cadena válida' if is_valid_chain else 'Cadena no válida'
    response = {
        'is_valid': is_valid_chain,
        'message': message
    }
    return jsonify(response), 200


# Obtener la cadena de bloques al completo
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response)


# Ejecutar la app
app.run(host='127.0.0.1', port='5000')
