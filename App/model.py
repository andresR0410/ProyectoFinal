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
from DataStructures import mapstructure as map
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
    tree = oms.newMap('RBT')
    gdir = g.newGraph(97, compareByKey, directed=True)
    tempHash = map.newMap(179, maptype='CHAINING', comparefunction=compareByKey)
    tempList = lt.newList('ARRAY')
    catalog = {'capacityMap':capacityMap, 'stationMap': stationMap,"dateTree": tree, 
    "GraphDirected":gdir, 'temperatureHash': tempHash, 'tempList':tempList}
    return catalog

def addToHash (catalog, row):
    capacity_station = (row['dock_count'],row['id']) 
    if map.contains(catalog['capacityMap'],row['city']):
        statcapList = map.get(catalog['capacityMap'],row['city'])
        lt.addFirst(statcapList,capacity_station)
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
            map.put(dateValue, StationInf, value+1)
        else:
            map.put(dateValue, StationInf, 1)
        totalValue = map.get(dateValue, 'total')
        totalValue += 1
        map.put(dateValue, 'total', totalValue)
        tree = oms.put(tree, date, dateValue, greater)
    else:
        DateValueMap = map.newMap(maptype='PROBING', comparefunction= compareByKey)
        map.put(DateValueMap, StationInf, 1)
        map.put(DateValueMap, 'total', 1)
        tree = oms.put(tree, date, DateValueMap, greater)

def addTempHash (catalog, row):
    hashTemp = catalog['temperatureHash']
    date = strToDate(row['date'], '%Y/%m/%d') #Convertir fecha a str
    if map.contains(catalog['temperatureHash'], row['mean_temperature_f']):
        dateIList = map.get(catalog['temperatureHash'], row['mean_temperature_f'])
        lt.addLast(dateIList, date) 
        map.put(catalog['temperatureHash'], row['temperatureHash'], dateIList)
    else:
        dateList = lt.newList('ARRAY')
        lt.addLast(dateList, date)
        map.put(hashTemp, row['mean_temperature_f'], dateList)

def tempAux (catalog):
    tempValues = map.keySet(catalog['temperaturaHash'])
    mergesort.mergesort(tempValues, greater)
    catalog['tempList'] = tempValues

def tripsPerTemperature(catalog, number):
    longList = lt.size(catalog['tempList'])
    leastTemp = lt.subList(catalog['tempList'],longList-number,number)
    mostTemp = lt.subList(catalog['tempList'], 1, number) #O(1) por ser array
    counter1 = 0
    counter2 = 0
    response1=''
    response2=''
    tripsMostTempDays = map.newMap(30, comparefunction=compareByKey)
    tripsLeastTempDays = map.newMap(30, comparefunction=compareByKey)

    while counter1<number:
        leastTempIterator = it.newIterator(leastTemp) #Iterar la lista con n menores temperaturas
        while it.hasNext(leastTempIterator):
            tempElement = it.next(leastTempIterator) #Temperatura
            dateListElement = map.get(catalog['temperatureHash'],tempElement)#Lista de todas las fechas para esa temperatura
            if number - lt.size(dateListElement) < counter1: 
                #si no se pueden agregar todas las fechas de esa temperatura sin alcanzar el n deseado
                n_dates = lt.subList(dateListElement, 1, number-counter1) #lista de las que si se pueden agragar
                n_iterator = it.newIterator(n_dates)
                while it.hasNext(n_iterator):
                    n_dateElement = it.next(n_iterator) #fecha a agregar
                    trips = oms.get(catalog['datesTree'], n_dateElement, greater) #hash de viajes de esa fecha
                    totaltrip = map.get(trips, 'total') #número de viajes totales en esa fecha
                    value = (tempElement, totaltrip) #tupla que se asigna como valor de cada fecha: temperatura, viajes totales
                    map.put(tripsLeastTempDays, n_dateElement, value)
                counter1 += lt.size(n_dates)#el número de fechas que se agregó se suma al counter
            else:
                #si se pueden agregar todas las fechas de esa temperatura sin alcanzar el n deseado
                n_dates = dateListElement #se recorre la lista completa
                n_iterator = it.newIterator(n_dates)
                while it.hasNext(n_iterator):
                    n_dateElement = it.next(n_iterator) #fecha a agregar
                    trips = oms.get(catalog['datesTree'], n_dateElement, greater)
                    totaltrip = map.get(trips, 'total')
                    value = (tempElement, totaltrip)
                    map.put(tripsLeastTempDays, n_dateElement, value)
                counter1 += lt.size(dateListElement)

    while counter2<number:
        mostTempIterator = it.newIterator(mostTemp) #Iterar la lista con n temperaturas más altas
        while it.hasNext(mostTempIterator):
            tempElement = it.next(mostTempIterator)
            dateListElement = map.get(catalog['temperatureHash'],tempElement)#Lista de todas las fechas para esa temperatura
            if number - lt.size(dateListElement) < counter2:
                #si no se pueden agregar todas las fechas de esa temperatura sin alcanzar el n deseado
                n_dates = lt.subList(dateListElement, 1, number-counter2)
                n_iterator = it.newIterator(n_dates)
                while it.hasNext(n_iterator):
                    n_dateElement = it.next(n_iterator)
                    value = oms.get(catalog['datesTree'], n_dateElement, greater)
                    value = map.get(value, 'total')
                    value = (tempElement, value)
                    map.put(tripsMostTempDays, n_dateElement, value)
                counter2 += lt.size(n_dates)
            else:
                #si se pueden agregar todas las fechas de esa temperatura sin alcanzar el n deseado
                n_dates = dateListElement
                n_iterator = it.newIterator(n_dates)
                while it.hasNext(n_iterator):
                    n_dateElement = it.next(n_iterator)
                    value = oms.get(catalog['datesTree'], n_dateElement, greater)
                    value = map.get(value, 'total')
                    value = (tempElement, value)
                    map.put(tripsMostTempDays, n_dateElement, value)
                counter2 += lt.size(dateListElement)

    if not map.isEmpty(tripsMostTempDays):
        tempList= map.keySet(tripsMostTempDays)
        iteratemp=it.newIterator(tempList)
        while it.hasNext(iteratemp):
            tempKey = it.next(iteratemp)
            response1 += str(tempKey) + ':' + str(map.get(tripsMostTempDays,tempKey)) + " "    
    if not map.isEmpty(tripsLeastTempDays):
        tempList= map.keySet(tripsLeastTempDays)
        iteratemp=it.newIterator(tempList)
        while it.hasNext(iteratemp):
            tempKey = it.next(iteratemp)
            response2 += str(tempKey) + ':' + str(map.get(tripsLeastTempDays,tempKey)) + " "
    return response1, response2

def sortHash (catalog):
    #Iterar tabla de hash, extraer lista de llaves, ordenar cada lista de tuplas con mergeSort
    citiesList = map.keySet(catalog['capacityMap'])
    citiesIter = it.newIterator(citiesList)
    while it.hasNext(citiesIter):
        i_city = it.next(citiesIter)
        stationCapacityList = map.get(catalog['capacityMap'], i_city)
        mergesort.mergesort(stationCapacityList, compareByTuple)

def addDirectedNode (catalog, row):
    """
    Adiciona un nodo para almacenar un libro o usuario 
    """
    source = row['src']
    dest = row['dst']
    if not g.containsVertex(catalog['GraphDirected'], source):
        g.insertVertex (catalog['GraphDirected'], source)
    if not g.containsVertex(catalog['GraphDirected'], dest):
        g.insertVertex (catalog['GraphDirected'], dest)

def addDirectedEdge (catalog, row):
    """
    Adiciona un enlace para almacenar una revisión
    """
    g.addEdge (catalog['GraphDirected'], row['src'], row['dst'], float(row['duration']))

#funciones de consulta
def mostCapacity(catalog, city, number_capacities):
    rawMap = catalog['capacityMap']
    cityCapacityMap = map.get(rawMap, city)
    TopN = cityCapacityMap[-number_capacities:]
    LessN = cityCapacityMap[:number_capacities-1]
    return TopN, LessN

def tripCityforDates (catalog, start_date, end_date):
    start_date=strToDate(start_date, '%m/%d/%Y') #Convertir fecha a str
    end_date=strToDate(end_date, '%m/%d/%Y') #Convertir fecha a str
    dateList = oms.valueRange(catalog['dateTree'], start_date, end_date, greater) #Lista de llaves entre las fechas dadas 
    response=''
    tripsCityDays = map.newMap(capacity=11, maptype='CHAINING') #Se almacenan
    if dateList:
        iteraDate=it.newIterator(dateList)
        while it.hasNext(iteraDate):
            dateElement = it.next(iteraDate)
            if oms.get(catalog['dateMap'],dateElement, greater):#Si el nodo tiene un valor asociado
                    if map.isEmpty(tripsCityDays):#Si cities está vacío, se le asigna el map de accidentes por ciudad del primer nodo
                        tripsCityDays = oms.get(catalog['dateMap'], dateElement, greater)
                    else: #De lo contrario, se compara cada ciudad del map de cada nodo con el map 
                        ciudadesNodo = map.keySet(dateElement)#Lista de las ciudades que tuvieron accidentes en esa fecha(nodo)
                        ciudadesCities = map.keySet(tripsCityDays)
                        iteraCiudades = it.newIterator(ciudadesNodo)
                        while it.hasNext(iteraCiudades):
                            ciudadElement=it.next(iteraCiudades)# que está en el map de cada nodo
                            if ciudadElement:
                                if lt.isPresent(ciudadesCities, ciudadElement, compareByKey): #Se verifica si la ciudad está en los valores del map 
                                    num=map.get(tripsCityDays, ciudadElement)
                                    num+=map.get(dateElement, ciudadElement)
                                    map.put(tripsCityDays, ciudadElement, num)
                                else:
                                    num= map.get(dateElement, ciudadElement)
                                    map.put(dateElement, ciudadElement, num)

    if not map.isEmpty(tripsCityDays):
        cityList= map.keySet(tripsCityDays)
        iteracity=it.newIterator(cityList)
        while it.hasNext(iteracity):
            cityKey = it.next(iteracity)
            response += str(cityKey) + ':' + str(map.get(tripsCityDays,cityKey)) + " "
        return response
    return None

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

def strToDate(date_string, format):
    
    try:
        # date_string = '2016/05/18 13:55:26' -> format = '%Y/%m/%d %H:%M:%S')
        return datetime.strptime(date_string,format)
    except:
        return datetime.strptime('1900', '%Y')