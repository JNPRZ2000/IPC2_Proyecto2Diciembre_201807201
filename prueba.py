import json
if __name__ == "__main__":
    dictionary = dict()
    json_f = open("Player\json_object.json","r")
    json_f2 = open("Player\json_object2.json", "r")
    json_o = json_f.read()
    json_o2 = json_f2.read()
    json_f.close()
    json_f2.close()
    auxdict = json.loads(json_o)
    auxdict2 = json.loads(json_o2)
    for key_lista in auxdict2:
        if key_lista in auxdict:
            auxdict[key_lista].extend(auxdict2[key_lista])
        else:
            auxdict[key_lista] = auxdict2[key_lista]            
    dictionary = auxdict
    print("Diccionario: {}".format(dictionary))
<!--{% for clave, valor in element.items %}
                        {% ifequal clave 'cancion' %}
                            <td>{{valor}}</td>
                        {% endifequal %}
                        {% ifequal clave 'album' %}
                            <td>{{valor}}</td>
                        {% endifequal %}
                        {% ifequal clave 'artista' %}
                            <td>{{valor}}</td>
                        {% endifequal %}
                        {% ifequal clave 'reproducciones' %}
                            <td>{{valor}}</td>
                        {% endifequal %}
                    {% endfor %}-->