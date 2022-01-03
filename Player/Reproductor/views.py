from typing import Dict, OrderedDict
from django.shortcuts import redirect, render
from django.http import HttpResponse
import re
import copy
import xml.etree.ElementTree as ET
import json
import requests


class Front:
    def __init__(self):
        self.xml = ''
        self.json = ''
        self.est_listas = dict()
        self.est_artistas = dict()
        self.est_canciones = dict()
class Cancion:
    def __init__(self,cancion,album,artista,reproducciones,ruta,imagen):
        self.cancion = cancion
        self.album = album
        self.artista = artista
        self.reproducciones = reproducciones
        self.ruta = ruta
        self.imagen = imagen
f = Front()
endpoint = "http://127.0.0.1:5000/{}"
# Create your views here.
def up_edit_csv(request):
    return render(request, 'up_edit_csv.html')

def up_edit_xml(request):
    xml = copy.copy(f.xml)
    f.xml = ''
    return render(request, 'up_edit_xml.html', {"xml": xml})

def up_file_xml(request):
    if request.POST["subfile"]:
        document = request.FILES['upload-xml']
        f.xml = document.read().decode()
        return redirect("xml")
def edit_file_xml(request):
    if request.POST["subtext"]:
        xml = request.POST["text-xml"]
        root = ET.fromstring(xml)
        dict_aux = dict()
        for listas in root.iter('ListasReproduccion'):
            for lista in listas.iter('Lista'):
                dict_aux[lista.attrib['nombre']] = []
                for cancion in lista.iter('cancion'):
                    cancion_ = cancion.attrib["nombre"]
                    album_ = ""
                    artista_ = ""
                    reproducciones_ = ""
                    ruta_ = ""
                    imagen_ = "" 
                    for artista,album,reproducciones,imagen,ruta in zip(
                        cancion.iter("artista"),cancion.iter("album"),cancion.iter("vecesReproducida"),
                        cancion.iter("imagen"),cancion.iter("ruta")):
                        album_ += str(album.text)
                        artista_ += str(artista.text)
                        reproducciones_ += str(reproducciones.text)
                        ruta_ += str(ruta.text)
                        imagen_ += str(imagen.text)
                    songdict = {"cancion": cancion_, "album": album_, "artista": artista_, "reproducciones": int(reproducciones_),
                    "ruta": ruta_, "imagen": imagen_}
                    dict_aux[lista.attrib['nombre']].append(songdict)
        json_aux = json.dumps(dict_aux)
        with open("json_object.json","w") as file:
            file.write(json_aux)
            file.close()
        url = endpoint.format("/receive-json")
        receive_json = requests.post(url, json= json_aux
        )
        f.json = receive_json.json()
        print("receive: {}".format(receive_json.json()))
        tree = ET.fromstring(xml)
        tree = ET.ElementTree(tree)
        tree.write("CSV Convertido.xml", encoding ='utf-8', xml_declaration = True)
        return redirect('viewcontent')

def view_content(request):
    diccionario = (f.json)
    url = endpoint.format("/peticion")
    peticion = requests.post(url)
    diccionario = peticion.json()
    return render(request, 'view_content.html', {"dict":diccionario, "headers": ["cancion","album","artista","reproducciones"]})

def reproducir(request, lista):
    lis = str(lista)
    lis = lis.split("+")
    listR = lis[0]
    cancion = lis[1]
    album = lis[2]
    artista = lis[3]
    url = endpoint.format('/peticion')
    peticion = requests.post(url)
    diccionario = peticion.json()
    ruta = ""
    imagen = ""
    for keylist in diccionario:
        if keylist == listR:
            for song in diccionario[keylist]:
                if song["cancion"] == cancion:
                    song["reproducciones"] = int(song["reproducciones"]) + 1
                    ruta += str(song["ruta"])
                    imagen += str(song["imagen"])
    json_obj = json.dumps(diccionario)
    url = endpoint.format("/actualizacion")
    actualize = requests.post(url, json = json_obj)
    if listR in f.est_listas:
        f.est_listas[listR] += 1
    else:
        f.est_listas[listR] = 1
    if cancion in f.est_canciones:
        f.est_canciones[cancion] += 1
    else:
        f.est_canciones[cancion] = 1
    if artista in f.est_artistas:
        f.est_artistas[artista] += 1
    else:
        f.est_artistas[artista] = 1
    return render(request, 'reproducir.html',{'cancion':cancion,'album':album,'artista':artista, 'ruta': ruta, 'imagen': imagen})
def estadisticas(request):
    f.est_listas = OrderedDict(sorted(f.est_listas.items(), key = lambda x : x[1]))
    f.est_canciones = OrderedDict(sorted(f.est_canciones.items(), key = lambda x : x[1]))
    f.est_artistas = OrderedDict(sorted(f.est_artistas.items(), key = lambda x: x[1]))
    clavesLista = []
    valoresLista = []
    clavesCanciones = []
    valoresCanciones = []
    clavesArtistas = []
    valoresArtistas = []
    for lista, cancion, artista in zip(f.est_listas, f.est_canciones, f.est_artistas):
        clavesLista.append(lista)
        valoresLista.append(f.est_listas[lista])
        clavesCanciones.append(cancion)
        valoresCanciones.append(f.est_canciones[cancion])
        clavesArtistas.append(artista)
        valoresArtistas.append(f.est_artistas[artista])
    if len(clavesLista) > 5:
        clavesLista = clavesLista[(len(clavesLista)-6), (len(clavesLista)-1)]
        valoresLista = valoresLista[(len(clavesLista)-6), (len(clavesLista)-1)]
    if len(clavesCanciones) > 5:
        clavesCanciones = clavesCanciones[(len(clavesCanciones)-6), (len(clavesCanciones)-1)]
        valoresCanciones = valoresCanciones[(len(clavesCanciones)-6), (len(clavesCanciones)-1)]
    if len(clavesArtistas) > 5:
        clavesArtistas = clavesArtistas[(len(clavesArtistas)-6), (len(clavesArtistas)-1)]
        valoresArtistas = valoresArtistas[(len(clavesArtistas)-6), (len(clavesArtistas)-1)]
    dictEst = {"claveslista": clavesLista, "valoreslista": valoresLista, "clavescanciones": clavesCanciones,
    "valorescanciones": valoresCanciones, "clavesartistas":clavesArtistas, "valoresartistas": valoresArtistas}
    json_obj = json.dumps(dictEst)
    url = endpoint.format("/estadisticas")
    graph = requests.post(url, json = json_obj)    
    return render(request, 'estadisticas.html')
def info(request):
    return render(request, 'info.html')

def up_file_csv(request):
    if request.POST["subfile"]:
        document = request.FILES['upload-csv']
        csv = str(document.read().decode("UTF-8"))
        csv = csv.replace("\\","/")
        errores = validateCsv(csv)
        return render(request, "up_edit_csv.html", {"csv": csv, "errores": errores})
def edit_file_csv(request):
    if request.POST["subtext"]:
        csv = request.POST["text-csv"]
        errores = validateCsv(csv)
        if errores == '':
            f.xml = toXML(csv)
            return redirect("xml")
        else:
            return render(request, "up_edit_csv.html", {"csv": csv, "errores": errores})


def validateCsv(csv):
    lines = csv.split("\n")
    i = 0
    errores = ''
    for line in lines:
        if i == 0 or line == lines[-1]:
            pass
        else:
            contains = re.search(r"([a-zA-Zá-üÁ-Ü ]+),([a-zA-Zá-üÁ-Ü ]+),([a-zA-Zá-üÁ-Ü ]+),([a-zA-Zá-üÁ-Ü ]+),([\d+$]+)",line)
            if contains != None:
                pass
            else:
                errores += ' {},'.format(i)
                print("Linea con error: {}".format(line))
        i += 1
    return errores
def toXML(csv):
    csv = str(csv)
    csv = csv.replace('\\','/')
    diccionario = csv_to_dict(csv)
    xml = '<?xml version = "1.0" encoding = "UTF-8"?>\n'
    xml += "<ListasReproduccion>\n"
    root = ET.Element("ListasReproduccion")
    for key in diccionario:
        xml +='\t<Lista nombre = "{}">\n'.format(key)
        hijo = ET.SubElement(root,"Lista", nombre = "{}".format(key))
        for song in diccionario[key]:
            nieto = ET.SubElement(hijo, "cancion", nombre = "{}".format(song.cancion))
            ET.SubElement(nieto, "artista").text = "{}".format(song.artista)
            ET.SubElement(nieto, "album").text = "{}".format(song.album)
            ET.SubElement(nieto, "vecesReproducida").text = "{}".format(song.reproducciones)
            img = str(song.imagen)
            img = img.rstrip("\n")
            ET.SubElement(nieto, "imagen").text = '{}'.format(img)
            ET.SubElement(nieto, "ruta").text = "{}".format(song.ruta)
            xml += '\t\t<cancion nombre = "{}">\n'.format(song.cancion)
            xml += '\t\t\t<artista>{}</artista>\n'.format(song.artista)
            xml += '\t\t\t<album>{}</album>\n'.format(song.album)
            xml += '\t\t\t<vecesReproducida>{}</vecesReproducida>\n'.format(song.reproducciones)
            xml += '\t\t\t<imagen>{}</imagen>\n'.format(img)
            xml += '\t\t\t<ruta>{}</ruta>\n'.format(song.ruta)
            xml += '\t\t</cancion>\n'
        xml += '\t</Lista>\n'
    xml += "</ListasReproduccion>"
    tree = ET.ElementTree(root)
    tree.write("CSV Convertido.xml", encoding ='utf-8', xml_declaration = True)
    return xml
def csv_to_dict(csv):
    lines = csv.split("\n")
    i = 0
    diccionario = dict()
    for line in lines:
        if i == 0:
            pass
        elif line == lines[-1]:
            pass
        else:
            line = line.replace('\n','')
            elements = line.split(',')
            lista = elements[0]
            cancion = elements[1]
            artista = elements[2]
            album = elements[3]
            reproducciones = elements[4]
            ruta = elements[5]
            imagen = elements[6]
            newSong = Cancion(cancion,album,artista,reproducciones,ruta,imagen)
            if lista in diccionario:
                diccionario[lista].append(newSong)
            else:
                vector = []
                vector.append(newSong)
                diccionario[lista] = vector
        i += 1
    return diccionario
