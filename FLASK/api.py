from os import stat
from flask import Flask, request
from flask.wrappers import Response
from flask_cors import CORS
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
cors = CORS(app, resources = {r"/*":{"origin":"*"}})
class Back:
    def __init__(self):
        self.diccionario = dict()
b = Back()
@app.route("/receive-json", methods = ['POST'])
def getXMLPOSTXML():
    json_obj = request.json
    library = json.loads(json_obj)
    for key_lista in library:
        if key_lista in b.diccionario:
            b.diccionario[key_lista].extend(library[key_lista])
        else:
            b.diccionario[key_lista] = library[key_lista]
    json_return = json.dumps(b.diccionario)
    return Response(json_return)
@app.route("/peticion", methods = ['POST'])
def peticion():
    json_return = json.dumps(b.diccionario)
    return Response(json_return)
@app.route('/actualizacion', methods = ['POST'])
def actualizacion():
    json_obj = request.json
    library = json.loads(json_obj)
    b.diccionario = library
    return Response(status=200)
@app.route('/estadisticas', methods = ['POST'])
def estadisticas():
    json_obj = request.json
    library = json.loads(json_obj)
    fig1, ax1 = plt.subplots()
    ax1.set_ylabel('Repitencias')
    ax1.set_title('Listas Más Escuchadas')
    plt.bar(library["claveslista"], library["valoreslista"])
    plt.savefig('Player\Reproductor\static\\est_listas.png')
    fig2, ax2 = plt.subplots()
    ax2.set_ylabel('Repitencias')
    ax2.set_title('Canciones Más Escuchadas')
    plt.bar(library["clavescanciones"], library["valorescanciones"])
    plt.savefig('Player\Reproductor\static\\est_canciones.png')
    valoresartistas = library["valoresartistas"]
    suma = sum(valoresartistas)
    for valor in valoresartistas:
        valor = float(valor/suma)
    fig3, ax3 = plt.subplots()
    ax3.pie(valoresartistas, labels = library["clavesartistas"], autopct = '%1.1f%%', shadow = True, startangle = 90)
    ax3.axis('equal')
    plt.title("Artistas Más Escuchados")
    plt.legend()
    plt.savefig('Player\Reproductor\static\\est_artistas.png')
    return Response(status = 200)

if __name__ == "__main__":
    app.run(debug = True)
    pass