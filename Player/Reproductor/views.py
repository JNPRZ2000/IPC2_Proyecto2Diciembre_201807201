from django.shortcuts import redirect, render
from django.http import HttpResponse
import re
import copy
import xml.etree.ElementTree as ET
class Front:
    def __init__(self):
        self.xml = ''
class Cancion:
    def __init__(self,cancion,album,artista,reproducciones,ruta,imagen):
        self.cancion = cancion
        self.album = album
        self.artista = artista
        self.reproducciones = reproducciones
        self.ruta = ruta
        self.imagen = imagen
f = Front()
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
        tree = ET.fromstring(xml)
        tree = ET.ElementTree(tree)
        tree.write("CSV Convertido.xml", encoding ='utf-8', xml_declaration = True)
        return HttpResponse(xml)

def up_file_csv(request):
    if request.POST["subfile"]:
        document = request.FILES['upload-csv']
        #csv = document.read().decode("utf-8")
        csv = str(document.read().decode("UTF-8"))
        print("Csv: {}".format(csv))
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
            ET.SubElement(nieto, "imagen").text = '{}'.format(song.imagen)
            ET.SubElement(nieto, "ruta").text = "{}".format(song.ruta)
            xml += '\t\t<cancion nombre = "{}">\n'.format(song.cancion)
            xml += '\t\t\t<artista>{}</artista>\n'.format(song.artista)
            xml += '\t\t\t<album>{}</album>\n'.format(song.album)
            xml += '\t\t\t<vecesReproducida>{}</vecesReproducida>\n'.format(song.reproducciones)
            xml += '\t\t\t<imagen>{}</imagen>\n'.format(song.imagen)
            xml += '\t\t\t<ruta>{}</ruta>\n'.format(song.ruta)
            xml += '\t\t</Cancion>\n'
        xml += '\t</Lista>\n'
    xml += "</ListasReproduccion>"
    tree = ET.ElementTree(root)
    tree.write("CSV Convertido.xml", encoding ='utf-8', xml_declaration = True)
    #ith open('csv_to_xml.xml', 'w') as f:
    #    f.write(xml)
    #    f.close()
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