from flask import Flask, request
from flask.wrappers import Response
from flask_cors import CORS
import json
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

    print("DICCIONARIO: {}".format(library))
    return Response(json_return)

if __name__ == "__main__":
    app.run(debug = True)
    pass