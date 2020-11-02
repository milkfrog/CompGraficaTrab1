from Objetos import *
from io import StringIO

def criaObjetoDeArquivoObj(stream: StringIO):
    lines = stream.readlines()
    numOfVertices = len(lines) - 1

    coordenadas = []
    for line in lines:
        if line[0] == "o":
            nome = line.split(" ")[1]
        elif line[0] == "v":
            vertice = line.split(" ")
            coordenadas.append(Coordenada(float(vertice[1]), float(vertice[2]), float(vertice[3])))

    if numOfVertices == 1:
        return Ponto(nome, coordenadas)
    elif numOfVertices == 2:
        return Reta(nome, coordenadas)
    elif numOfVertices > 2:
        return Wireframe(nome, coordenadas)
    else:
        return None

def traduzParaFormatoObj(objeto):
    objStream = StringIO()
    objStream.write("o " + objeto.nome + "\n")
    cooredenadas = objeto.coordenadas

    for coordenada in cooredenadas:
        coordenadaComoString = str(coordenada.x) + " " + str(coordenada.y) + " " + str(coordenada.z)
        objStream.write("v " + coordenadaComoString + "\n")
    
    return objStream