import os

import flask
from flask import Flask, jsonify, request

import elasticsearch
from elasticsearch import Elasticsearch

import elasticsearch.exceptions

from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.connections import connections


###  Connexion Elasticsearch  ###
elasticClient = Elasticsearch(
    'https://yvwwd7r6g7:lue555jb9h@quchempedia-9079321169.eu-central-1.bonsaisearch.net')

app = Flask(__name__)


###  Route pour la recherche par formule  ###
@app.route('/api/search/<formula>', methods=['GET'])
def search_molecule(formula):
    """Return the list of molecules which contains the formula given."""
    body = {
        "query": {
            "match_phrase": {
                "molecule.formula": formula
            }
        }
    }

    results = elasticClient.search(index='molecules', body=body)
    return jsonify(results['hits']['hits']), 200


###  Route pour retrouver une molécule avec son ID  ###
@app.route('/api/details/<id_mol>', methods=['GET'])
def details_molecule(id_mol):

    try:
        results = elasticClient.get(
            index='molecules', doc_type='molecule', id=id_mol)
        return jsonify(results), 200
    except elasticsearch.exceptions.NotFoundError:
        return jsonify({'Error': 'Molecule with id = \'' +
                        id_mol + '\' does not exists!'}), 404


###  Route pour l'ajout d'une molécule  ###
@app.route('/api/add', methods=['POST'])
def add_molecule():

    body = request.json

    if (body == None):
    	return jsonify({'Error': 'There is no body provided for the molecule!'}), 404

    results = elasticClient.index(
        index='molecules', doc_type='molecule', body=body)
    add_log_file(results["_id"])
    return jsonify(results)


###  Route pour la suppression d'une molécule  ###
@app.route('/api/delete/<id_mol>', methods=['DELETE'])
def delete_molecule(id_mol):

    try:
        results = elasticClient.delete(
            index='molecules', doc_type='molecule', id=id_mol)
        delete_log_file(id_mol)
        return jsonify(results), 200
    except elasticsearch.exceptions.NotFoundError:
        return jsonify({'Error': 'Molecule with id = \'' +
                        id_mol + '\' does not exists!'}), 404


# Fonction pour la création d'un fichier de log lors de l'ajout de
# molécules  ###
def add_log_file(id_mol):

    root_path = 'data_dir/'
    log_path = ''

    for char in id_mol:
        log_path += char
        log_path += '/'

    root_path += log_path
    os.makedirs(root_path)

    log_file = open(root_path + "data.log", "x")
    log_file.write(id_mol)


###  Fonction pour la suppression d'un fichier de log  ###
def delete_log_file(id_mol):

    root_path = 'data_dir/'
    log_path = ''

    for char in id_mol:
        log_path += char
        log_path += '/'

    root_path += log_path
    log_file_path = root_path + 'data.log'

    if os.path.exists(log_file_path):
        os.remove(log_file_path)
        delete_empty_path(root_path[:-1])


###  Fonction pour supprimer les dossiers vides  ###
def delete_empty_path(path):

    if len(os.listdir(path)) == 0:
        os.rmdir(path)
        delete_empty_path(path[:-2])
