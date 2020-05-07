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
import model
import csv
from ADT import list as lt
from ADT import map as map


from DataStructures import listiterator as it
from Sorting import mergesort as sort
from time import process_time


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Funcionaes utilitarias

def printList (lst):
    iterator = it.newIterator(lst)
    while  it.hasNext(iterator):
        element = it.next(iterator)
        result = "".join(str(key) + ": " + str(value) + ",  " for key, value in element.items())
        print (result)


# Funciones para la carga de datos 
def loadFlights (catalog, sep=';'):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por 
    cada uno de ellos, se crea un arbol de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    t1_start = process_time() #tiempo inicial
    nodesfile = cf.data_dir + 'flights_nodes.csv'
    edgesfile = cf.data_dir + 'flights_edges.csv'
    nodesdirectedfile= cf.data_dir + "flights_nodes_dir.csv"
    edgesdirectedfile= cf.data_dir +  "flights_edges_dir.csv"
    dialect = csv.excel()
    dialect.delimiter=sep
    with open(nodesfile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        t2_start = process_time() #tiempo inicial
        for row in spamreader:
            model.addNode(catalog, row)
        t2_stop = process_time() #tiempo final
    with open(edgesfile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        t3_start = process_time() #tiempo inicial
        for row in spamreader:
            model.addEdge(catalog, row)
    with open(nodesdirectedfile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        t2_start = process_time() #tiempo inicial
        for row in spamreader:
            model.addDirectedNode(catalog, row)
        t2_stop = process_time() #tiempo final
    with open(edgesdirectedfile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        t3_start = process_time() #tiempo inicial
        for row in spamreader:
            model.addDirectedEdge(catalog, row)
        t3_stop = process_time() #tiempo final
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga de grafo de vuelos",t1_stop-t1_start," segundos\n"
    "Tiempo de carga de nodos",t2_stop-t2_start,"segundos\n"
    "Tiempo de carga de arcos",t3_stop-t3_start,"segundos")   

def initCatalog ():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog



def loadData (catalog):
    """
    Carga los datos de los archivos en la estructura de datos
    """
    loadFlights(catalog)    

# Funciones llamadas desde la vista y enviadas al modelo


def countNodesEdges(catalog):
    t1_start = process_time() #tiempo inicial
    nodes, edges = model.countNodesEdges(catalog)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución de conteo de componentes conectados:",t1_stop-t1_start," segundos")
    return nodes, edges


def getShortestPath(catalog, vertices):
    t1_start = process_time() #tiempo inicial
    source=vertices.split(" ")[0]
    dst=vertices.split(" ")[1]
    path = model.getShortestPath(catalog, source, dst)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución de dijkstra: ",t1_stop-t1_start," segundos")
    return path

def getPath(catalog, vertices):
    t1_start = process_time() #tiempo inicial
    source=vertices.split(" ")[0]
    dst=vertices.split(" ")[1]
    path = model.getPath(catalog, source, dst)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución de dfs",t1_stop-t1_start," segundos")
    return path

def getPathLeastEdges(catalog, vertices):
    #llama a una nueva función en model que utiliza bfs enviando src y dst
    #retorna el camino
    t1_start = process_time() #tiempo inicial
    source=vertices.split(" ")[0]
    dst=vertices.split(" ")[1]
    path = model.shorterPath(catalog, source, dst)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución de dfs",t1_stop-t1_start," segundos")
    return path

def countCC(catalog):
    t1_start = process_time() #tiempo inicial
    ccs = model.countCC(catalog) 
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución de conteo de componentes conectados:",t1_stop-t1_start," segundos")
    return ccs

