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
booleano = False
print(booleano)
booleano += True
booleano += True
booleano += True
print(bool(booleano))