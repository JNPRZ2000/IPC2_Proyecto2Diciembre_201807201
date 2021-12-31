from django.http.response import HttpResponse
from django.shortcuts import redirect, render
import re
# Create your views here.
class Front:
    def __init__(self) -> None:
        self.carga = False
        self.errores = ''
        self.contenido = ''
        self.xml = ''
        self.csv = ''
        pass
front = Front()


def up_csv(request):
    if request.method == 'POST':
        front.errores = ''
        errores = ''
        front.contenido = ''
        document = request.FILES['file_csv']
        contenido = document.read().decode()
        front.contenido = contenido
        errored = False
        errores = 'Lineas con error:'
        lineas = contenido.split('n')
        i = 1
        for linea in lineas:
            if i == 1:
                pass
            else:
                contains = re.search(r"([a-zA-Zá-üÁ-Ü ]+),([a-zA-Zá-üÁ-Ü ]+),([a-zA-Zá-üÁ-Ü ]+),([a-zA-Zá-üÁ-Ü ]+),([\d+$]+)",linea)
                if contains != None:
                    elementos = linea.split(",")
                    print("Elemento {}: {}".format(i,elementos))
                else:
                    errores += " {}".format(i)
                    errored +=True
                i+=1
        if bool(errored) == True:
            front.errores = errores
        return redirect('/edit-csv/')
    else:
        return render(request, "up_csv.html")


def edit_csv(request):
    if request.method == 'POST':
        front.errores = ''
        document = request.POST["area-csv"]
        errores = ''
        front.contenido = ''
        contenido = document
        front.contenido = contenido
        errored = False
        errores = 'Lineas con error:'
        lineas = contenido.split('n')
        i = 1
        
        for linea in lineas:
            if i == 1:
                pass
            else:
                contains = re.search(r"([a-zA-Zá-üÁ-Ü ]+),([a-zA-Zá-üÁ-Ü ]+),([a-zA-Zá-üÁ-Ü ]+),([a-zA-Zá-üÁ-Ü ]+),([\d+$]+)",linea)
                if contains != None:
                    elementos = linea.split(",")
                    print("Elemento {}: {}".format(i,elementos))
                else:
                    errores += " {}".format(i)
                    errored +=True
                i+=1
        if bool(errored) == True:
            front.errores = errores
            render(request, 'edit_csv.html', {"contenido":front.contenido, "errores":front.errores})
        else:
            return redirect('/edit-xml/')
    else:
        return render(request, 'edit_csv.html', {"contenido":front.contenido, "errores:":front.errores})
def edit_xml(request):
    if request.method == 'POST':
        csv = front.contenido
    else:
        pass

def toXML(csv):
    lines = csv.split("\n")
    xml = '<? version = "1.0" encoding = "UTF-8" ?>'

class Cancion:
    def __init__(self,cancion,album,artista,reproducciones,ruta,imagen):
        self.cancion = cancion
        self.album = album
        self.artista = artista
        self.reproducciones = reproducciones
        self.ruta = ruta
        self.imagen = imagen