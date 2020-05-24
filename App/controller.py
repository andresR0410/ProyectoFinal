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
    hashValues = cf.data_dir + 'station.csv'
    tree =  cf.data_dir + 'trip.csv'
    temperatureHash = cf.data_dir + 'weather.csv'
    dialect = csv.excel()
    dialect.delimiter=sep
    with open(hashValues, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        t2_start = process_time() #tiempo inicial
        for row in spamreader:
            model.addToHash(catalog, row)
            model.addToStationHash(catalog,row)
        t2_stop = process_time() #tiempo final
    model.sortHash(catalog['capacityMap'])
    with open(tree, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        t3_start = process_time() #tiempo inicial
        for row in spamreader:
            model.addToTree(catalog, row)
        t3_stop = process_time() #tiempo final
    with open(temperatureHash, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        t4_start = process_time() #tiempo inicial
        for row in spamreader:
            model.addTempHash(catalog, row)
        t4_stop = process_time() #tiempo final
    model.tempAux(catalog)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga de tabla de hash (req1) de estaciones por capacidad por ciudad",t2_stop-t2_start," segundos\n"
    print("Tiempo de ejecución carga de todos los datos: ",t1_stop-t1_start," segundos\n")
     

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

def getShortestPath(catalog, vertices):
    t1_start = process_time() #tiempo inicial
    source=vertices.split(" ")[0]
    dst=vertices.split(" ")[1]
    path = model.getShortestPath(catalog, source, dst)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución de dijkstra: ",t1_stop-t1_start," segundos")
    return path

def mostCapacity (catalog, city, number_capacities):
    t1_start = process_time() #tiempo inicial
    mostCapacities = model.mostCapacity(catalog, city, number_capacities)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución de mostCapacity",t1_stop-t1_start," segundos")
    mostCapacities=('Top'+str(number_capacities)+': ',mostCapacities[0]+'\n'+ 'Less'+str(number_capacities)+': ',mostCapacities[1])
    return mostCapacities

def tripCityforDates (catalog, dates):
    t1_start = process_time() #tiempo inicial
    start_date=dates.split(" ")[0]
    end_date=dates.split(" ")[1]
    tripCitiesDates = model.tripCityforDates(catalog, start_date, end_date)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución de tripCityforDates: "t1_stop-t1_start," segundos")
    return tripCitiesDates

def tripsPerTemperatureDate(catalog, number):
    t1_start = process_time() #tiempo inicial
    tripCitiesDates = model.tripsPerTemperature(catalog, number)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución de tripsPerTemperaturaDate: "t1_stop-t1_start," segundos")
    return tripsTempDates