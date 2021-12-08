# importar las librerias
import datetime
import hashlib
import json
from flask import Flask, jsonify


# parte 1 - crear la cadena de bloques
class Blockchain:

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
# parte 2 - minado de un bloque de la cadena
