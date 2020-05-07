"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller 
import csv
from ADT import list as lt
from ADT import stack as stk
from ADT import orderedmap as map
from DataStructures import listiterator as it

import sys


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido al Laboratorio 9")
    print("1- Cargar información")
    print("2- Contar nodos y enlances cargados ")
    print("3- Obtener el camino de menor costo entre dos vértices usando Dijkstra (origen destino)")
    print("4- Contar componentes conectados en el grafo")
    print("5- Existe una ruta entre dos aeropuertos para un fecha determinada, volver (dfs)")
    print("6- Ruta con menos escalas entre dos aeropuertos (bfs)")
    print("0- Salir")


def initCatalog ():
    """
    Inicializa el catalogo
    """
    return controller.initCatalog()


def loadData (catalog):
    """
    Carga las bibliotecas en la estructura de datos
    """
    controller.loadData(catalog)


"""
Menu principal 
""" 
def main():
    while True: 
        printMenu()
        inputs =input("Seleccione una opción para continuar\n")
        if int(inputs[0])==1:
            print("Cargando información de los archivos ....")
            catalog = initCatalog ()
            loadData (catalog)
        elif int(inputs[0])==2:
            verticesNum, edgesNum = controller.countNodesEdges(catalog) 
            print("El grafo tiene: ", verticesNum," nodos y", edgesNum," enlaces")
        elif int(inputs[0])==3: #Requerimento 3
            vertices =input("Ingrese el vertice origen y destino\n")
            path = controller.getShortestPath(catalog,vertices)
            print("El camino de menor costo entre los vertices es:")
            totalDist = 0
            if path:
                while not stk.isEmpty(path):
                    step = stk.pop(path)
                    totalDist += step['weight']
                    print (step['vertexA'] + "-->" + step['vertexB'] + " costo: " + str(step['weight']))
            print ("Total: " + str (totalDist))
        elif int(inputs[0]==4): #Requerimento 1
            ccs = controller.countCC(catalog)
            print("El grafo tiene :", ccs, 'componentes conectados') 
        elif int(inputs[0]==5): #Requerimento 2
            vertices =input("Ingrese el vertice origen y destino\n")
            lst = controller.getPath(catalog,vertices)
            if lst:
                print("El camino entre los vertices es:",lst)
            else:
                print("No hay camino")
        elif int(inputs[0]==6):#Requerimento 4
            vertices =input("Ingrese el vertice origen y destino\n")
            leastPath=controller.getPathLeastEdges(catalog, vertices)
            if leastPath:
                print("El camino más corto entre los vértices es: ",leastPath)
        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    main()