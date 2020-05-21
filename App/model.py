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
from DataStructures import orderedmapstructure as oms
import Test.graph.dfs as dfs
import Test.graph.bfs as bfs
from Sorting import mergesort
from datetime import datetime
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
    stationMap = map.newMap(97,maptype='CHAINING',comparefunction=compareByKey)
    tree = oms.newMap()
    gdir = g.newGraph(97, compareByKey, directed=True)
    catalog = {'capacityMap':capacityMap, 'stationMap': stationMap,"dateTree": tree, "GraphDirected":gdir}
    return catalog

def addToHash (catalog, row):
    capacity_station = (row['dock_count'],row['id']) 
    if map.contains(catalog['capacityMap'],row['city']):
        statcapList = map.get(catalog['capacityMap'],row['city'])
        lt.addFirst(stationCapacityList,capacity_station)
    else:
        stationCapacityList = lt.newList('ARRAY')
        lt.addFirst(stationCapacityList,capacity_station)
        map.put(catalog['capacityMap'],row['city'], stationCapacityList)

def addToStationHash (catalog, row):
    value=(row['name'], row['city'])
    map.put(catalog['stationMap'], row['id'], value)
    
def addToTree (catalog, row):
    tree=catalog['dateTree'] #Árbol RBT ordenado por fecha
    date=strToDate(row['start_date'], '%m/%d/%Y') #Convertir fecha a str
    StationInf = map.get(catalog['stationMap'], row['start_station_id'])[1] #Ciudad de la estación 
    if oms.contains(tree, date, greater):
        dateValue = oms.get(tree, date, greater)
        if map.contains(dateValue, StationInf):
            value = map.get(dateValue, StationInf)
            dateValue = map.put(dateValue, StationInf, value+1)
        else:
            dateValue = map.put(dateValue, StationInf, 1)
        tree = oms.put(tree, date, dateValue, greater)
    else:
        DateValueMap = map.newMap(97, 'CHAINING', compareByKey)
        dateValue = map.put(DateValueMap, StationInf, 1)
        tree = oms.put(tree, date, dateValue, greater)

def strToDate(date_string, format):
    
    try:
        # date_string = '2016/05/18 13:55:26' -> format = '%Y/%m/%d %H:%M:%S')
        return datetime.strptime(date_string,format)
    except:
        return datetime.strptime('1900', '%Y')

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
    if not g.containsVertex(catalog['GraphDirected'], row['start_station_id']):
        g.insertVertex (catalog['GraphDirected'], row['start_station_id'])

def addDirectedEdge (catalog, row):
    """
    Adiciona un enlace para almacenar una revisión
    """
    g.addEdge (catalog['GraphDirected'], row['src'], row['dst'], float(row['duration']))

def mostCapacity(catalog, city, number_capacities):
    rawMap = catalog['capacityMap']
    cityCapacityMap = map.get(rawMap, city)
    TopN = cityCapacityMap[-number_capacities:]
    LessN = cityCapacityMap[:number_capacities-1]
    return TopN, LessN

def tripCityforDates (catalog, start_date, end_date):
    start_date=strToDate(start_date, '%m/%d/%Y') #Convertir fecha a str
    end_date=strToDate(end_date, '%m/%d/%Y') #Convertir fecha a str
    dateList = oms.valueRange(catalog['dateTree'], start_date, end_date, greater) #Valor o nodos? 
    counter = 0
    response=''
    #Corregir para datos actuales
    cities = map.newMap(capacity=97, maptype='CHAINING')
    if dateList:
        iteraDate=it.newIterator(dateList)
        while it.hasNext(iteraDate):
            dateElement = it.next(iteraDate)
            if dateElement['date']:#Si el nodo tiene dicho map
                    if map.isEmpty(cities):#Si cities está vacío, se le asigna el map de accidentes por ciudad del primer nodo
                        cities=dateElement['cityMap']
                    else: #De lo contrario, se compara cada ciudad del map de cada nodo con el map cities
                        ciudadesNodo=map.keySet(dateElement['cityMap'])#Lista de las ciudades que tuvieron accidentes en esa fecha(nodo)
                        ciudadesCities=map.keySet(cities)
                        iteraCiudades=it.newIterator(ciudadesNodo)
                        while it.hasNext(iteraCiudades):
                            ciudadElement=it.next(iteraCiudades)#Nombre de la ciudad que está en el cityMap de cada nodo
                            if ciudadElement:
                                if lt.isPresent(ciudadesCities, ciudadElement, compareByStr): #Se verifica si la ciudad está en los valores del map cities
                                    num=map.get(cities, ciudadElement, compareByKey)
                                    num+=map.get(dateElement['cityMap'], ciudadElement, compareByKey)
                                    map.put(cities, ciudadElement, num, compareByKey)
                                else:
                                    num=map.get(dateElement['cityMap'],ciudadElement,compareByKey)
                                    map.put(cities, ciudadElement, num, compareByKey)

    if not map.isEmpty(cities):
        cityList= map.keySet(cities)
        iteracity=it.newIterator(cityList)
        while it.hasNext(iteracity):
            cityKey = it.next(iteracity)
            response += str(cityKey) + ':' + str(map.get(cities,cityKey,compareByKey)) + " "
        return counter, response
    return None

def getShortestPath(catalog, src, dst):
    pass



# Funciones de comparacion

def compareByKey (key, element):
    return  (key == element['key'] )

def compareByTuple (tup1, tup2):
    if tup1[0]>tup2[0]:
        return 1
    if tup1[0]<tup2[0]:
        return -1

def greater (key1, key2):
    if ( key1 == key2):
        return 0
    elif (key1 < key2):
        return -1
    else:
        return 1