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
from ADT import list as lt
from ADT import graph as g
from ADT import map as map
from ADT import list as lt
from DataStructures import listiterator as it
from datetime import datetime
from DataStructures import dijkstra as dj 
import Test.graph.dfs as dfs
import Test.graph.bfs as bfs
from Sorting import mergesort
"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores 
y otra para géneros
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo y retorna el catalogo inicializado.
    """
    capacityMap = map.newMap(maptype='PROBING',comparefunction=compareByKey)
    catalog = {'capacityMap':capacityMap}
    return catalog

def addToHash (catalog, row):
    capacity_station = (row['dock_count'],row['name'])
    if map.contains(catalog['capacityMap'],row['city']):
        statcapList = map.get(catalog['capacityMap'],row['city'])
        lt.addFirst(stationCapacityList,capacity_station)
    else:
        stationCapacityList = lt.newList('ARRAY')
        lt.addFirst(stationCapacityList,capacity_station)
        map.put(catalog['capacityMap'],row['city'], stationCapacityList)
        # FALTA ALGORITMO DE ORDENAMIENTO DE LISTAS

def sortHash (catalog):
    #Iterar tabla de hash, extraer lista de llaves, ordenar cada lista de tuplas con mergeSort
    citiesList = map.keySet(catalog['capacityMap'])
    citiesIter = it.newIterator(citiesList)
    while it.hasNext(citiesIter):
        i_city = it.next(citiesIter)
        stationCapacityList = map.get(catalog['capacityMap'], i_city)
        mergesort.mergesort(stationCapacityList, compareByKey) #Revisar compareFunction

def addDirectedNode (catalog, row):
    """
    Adiciona un nodo para almacenar un libro o usuario 
    """
    if not g.containsVertex(catalog['GraphDirected'], row['VERTEX']):
        g.insertVertex (catalog['GraphDirected'], row['VERTEX'])

def addDirectedEdge (catalog, row):
    """
    Adiciona un enlace para almacenar una revisión
    """
    g.addEdge (catalog['GraphDirected'], row['SOURCE'], row['DEST'], float(row['ARRIVAL_DELAY']))

def getPath (catalog, source, dst):
    """
    Retorna el camino, si existe, entre vertice origen y destino
    """
    print("vertices: ",source,", ",dst)
    graph = catalog['Graph']
    # ejecutar dfs desde source
    search= dfs.newDFS(graph, source)
    # obtener el camino hasta dst
    response = ''
    path = dfs.pathTo(search, dst)
    if path:
        iteraPath=it.newIterator(path)
        while it.hasNext(iteraPath):
            Vertex = it.next(iteraPath)
            response += Vertex + '\n'
        return response
    return None
    # retornar el camino
    
def shorterPath (catalog, source, dst):
    print("vertices: ",source,", ",dst)
    graph = catalog['Graph']
    # ejecutar dfs desde source
    search= bfs.newBFS(graph, source)
    # obtener el camino hasta dst
    response = ''
    t1_start = process_time() #tiempo inicial
    path = bfs.pathTo(search, dst)
    if path:
        iteraPath=it.newIterator(path)
        while it.hasNext(iteraPath):
            Vertex = it.next(iteraPath)
            response += Vertex + '\n'
        return response
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución de pathTo:",t1_stop-t1_start," segundos")
    return None
    # retornar el camino
# Funciones de comparacion

def compareByKey (key, element):
    return  (key == element['key'] )