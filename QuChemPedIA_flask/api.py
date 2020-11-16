from flask import Flask, json, request,render_template
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from elasticsearch_dsl.connections import connections

#es = Elasticsearch(['https://yvwwd7r6g7:lue555jb9h@quchempedia-9079321169.eu-central-1.bonsaisearch.net:433'])
# Connexion au client Elasticsearch
client = Elasticsearch(
    'https://yvwwd7r6g7:lue555jb9h@quchempedia-9079321169.eu-central-1.bonsaisearch.net')

app = Flask(__name__)


# Route pour la recherche de molécule
@app.route('/API/recherche')
def recherche():
    query = request.args.get('q')
    type  = request.args.get('type')
    liste = []

    s = Search(using = client, index = "molecules", doc_type = "molecule")
    s = s.query(
        {"regexp": {"molecule.formula": '[a-zA-Z0-9]*' + query + '[a-zA-Z0-9]*'}})
    #s = s.query('regexp',formula='[a-z0-9]'+query+'[a-z0-9]*')
    mol = s.execute()
    if mol.hits.total.value <= 0:
        return render_template('error/blade404.html')
    else:
        for molecules in s.execute():
            dict = {
                "id": molecules.meta.id,
                "formule": molecules.molecule.formula,
                "inchi": molecules.molecule.inchi,
                "nb_heavy_atoms": molecules.molecule.nb_heavy_atoms,
                "charge": molecules.molecule.charge,
                "total_molecular_energy": molecules.results.wavefunction.total_molecular_energy,
                "multiplicity": molecules.molecule.multiplicity,
            }
            liste.append(dict)

        response = app.response_class(
            response = json.dumps(mol.to_dict(), indent=4),
            mimetype = 'application/json'
        )
        return response

    # Route pour le détail d'une molécule


@app.route('/API/detail')
def detail():
    identifiant = request.args.get('id')
    s   = Search(using = client, index = "molecules", doc_type = "molecule")
    s   = s.query('match', _id=identifiant)
    try:
        mol = s.execute()[0].to_dict()
    except Exception as e:
        return render_template('error/blade404.html')

    response = app.response_class(
        response = json.dumps(mol, indent=4),
        mimetype = 'application/json'
    )
    return response


@app.route('/API/recherche_partielle')
def recherche_partielle():

    query = request.args.get('q')
    response = []
    s = Search(using = client, index = "molecules", doc_type = "molecule")

    if query.find('*') != -1 or query.find('_') != -1:
        query = query.replace("*", "[1-9]+")
        query = query.replace("_", "[a-zA-Z1-9]*")
        s     = s.query({"regexp": {"molecule.formula": query}})

    else:
        #query = query.replace("?","[1-9]+")
        s = s.query(
            {"regexp": {"molecule.formula": '[a-zA-Z0-9]*' + query + '[a-zA-Z0-9]*'}})

    molecules = s.execute()

    for molecule in s.execute():
        response.append(molecule.molecule.to_dict())

    response = sorted(response, key=lambda x: len(x["formula"]))

    response = app.response_class(
        response = json.dumps(response, indent=4),
        mimetype = 'application/json'
    )

    return response
