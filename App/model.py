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
    graph = g.newGraph(111353 ,compareByKey, directed=False)
    graphdi=g.newGraph(111353 ,compareByKey, directed=True)
    catalog = {'Graph':graph,'GraphDirected':graphdi}    
    return catalog

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

def addNode (catalog, row):
    """
    Adiciona un nodo para almacenar un libro o usuario 
    """
    if not g.containsVertex(catalog['Graph'], row['VERTEX']):
        g.insertVertex (catalog['Graph'], row['VERTEX'])

def addEdge (catalog, row):
    """
    Adiciona un enlace para almacenar una revisión
    """
    g.addEdge (catalog['Graph'], row['SOURCE'], row['DEST'], row['ARRIVAL_DELAY'])

def countNodesEdges (catalog):
    """
    Retorna la cantidad de nodos y enlaces del grafo de revisiones
    """
    nodes = g.numVertex(catalog['Graph'])
    edges = g.numEdges(catalog['Graph'])

    return nodes,edges

def getShortestPath (catalog, source, dst):
    """
    Retorna el camino de menor costo entre vertice origen y destino, si existe 
    """
    print("vertices: ",source,", ",dst)
    dis=dj.newDijkstra(catalog["GraphDirected"],source)
    path=dj.pathTo(dis,dst)
    # ejecutar Dijkstra desde source
    # obtener el camino hasta dst
    # retornar el camino
    return path

def countCC(catalog):
    return dfs.countCC(catalog['Graph'])

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

