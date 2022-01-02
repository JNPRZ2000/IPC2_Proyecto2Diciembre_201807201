import re
class Cancion:
    def __init__(self, artista, album, reproducciones, imagen, ruta, nombre) -> None:
        self.artista = artista
        self.album = album
        self.reproducciones = reproducciones
        self.imagen = imagen
        self.ruta = ruta
        self.nombre = nombre
    def __str__(self):
        return "Artista: {}  Album: {}   Canción: {}".format(self.artista,self.album,self.nombre)        

#match = re.match(r"([a-zA-Z]+),([a-zA-Z]+),([a-zA-Z]+),([a-zA-Z]+),([0-9]+)","NombreLista,NombreCancion,NombreArtista,NombreAlbum,001")
#if match ==  None:
#    print("F")
#else:
#    print("Match: {}".format(match.group(2)))
#cadena = "lista,cancion,artista,album,53,direccion.mp3,imagen.jpg"
#er = r"([a-zA-Z]+),([a-zA-Z]+),([a-zA-Z]+),([a-zA-Z]+),(\d+$),([a-zA-Z_\s/\\ñÑáéíóúÁÉÍÓÚ]+(\.mpg))"
#match = re.match(er,"lista,cancion,artista,album,10,c/carpeta/folder/cancion.mpg")
#if match == None:
#    print("No hizo match")
#else:
#    print("Match: {}".format(match))
#match = re.match(r"[a-zA-Z_\s/\\ñÑáéíóúÁÉÍÓÚ]+(\.mp3)","ruta\dir\cancion.mp3")   c:/carpeta/folder/cancion.mp3,c:/carpeta/folder/imagen.jpg
#print(match)c:/carpeta1/folder/cancion.mp3 //,([á-üÁ-Ü\w\s_:\.3]+) 
#cadena = "lista,cancion,artista,album,10,dir"
#contains = re.search(r"([a-zA-Z]+),([a-zA-Zá-ü]+),([a-zA-Z]+),([a-zA-Z]+),([\d+$]+)",cadena)
#print("Contains: {}".format(contains))
'''file = open("D:\Cursos\DICIEMBRE_2021\IPC2\LAB\PROYECTO 2\IPC2_Proyecto2Diciembre_201807201\prueba.csv","r")
csv = file.read()
file.close()
csv = csv.split("\n")
i = 0
diccionario = dict()
for line in csv:
    if i == 0:
        pass
    else:
        elements = line.split(',')
        lista = elements[0]
        cancion = elements[1]
        artista = elements[2]
        album = elements[3]
        reproducciones = elements[4]
        ruta = elements[5]
        imagen = elements[6]
        newSong = Cancion(artista,album,reproducciones,imagen,ruta,cancion)
        if lista in diccionario:
            diccionario[lista].append(newSong)
        else:
            vector = []
            vector.append(newSong)
            diccionario[lista] = vector
    i+=1
print("Diccionario: ")
print("Dict: {}".format(diccionario.items()))
print("Recorriendo Diccionario")
for key in diccionario:
    print("Key: {}".format(key))
    for song in diccionario[key]:
        print("\tSong: {}".format(song.nombre))

import xml.etree.ElementTree as ET
f = open('Player\Player\CSV Convertido.xml', "r")
fr = f.read()
f.close()
cont = ET.fromstring(fr)
cont2 = ET.tostring(cont)
print("Contenido: {}".format(cont2))'''
f = open("Player\CSV Convertido.xml", "r")
xml = f.read()
print("XML: {}".format(xml))
import xml.etree.ElementTree as ET
tree = ET.parse("Player\CSV Convertido.xml")
print("\nTree: {}".format(tree))
f.close()
        