import unittest
import config
from DataStructures import edge as e
from DataStructures import listiterator as it
from ADT import graph as g
from ADT import queue as q
from ADT import list as lt
import dfs
import bfs


class GraphTest (unittest.TestCase):

    def setUp (self):
        pass



    def tearDown (self):
        pass

    def comparenames (self, searchname, element):
        return (searchname == element['key'])

    def comparelst (self, searchname, element):
        return (searchname == element)


    def test_newEdge (self):
        edge = e.newEdge (1,1,1)
        print (edge)


    def test_edgeMethods (self):
        edge = e.newEdge ('Bogota','Cali')

        print (e.either(edge))
        print (e.other(edge, e.either(edge)))
        print (e.weight(edge))


    def test_insertVertex (self):
        graph = g.newGraph(7,self.comparenames)

        g.insertVertex (graph, 'Bogota')
        g.insertVertex (graph, 'Yopal')
        g.insertVertex (graph, 'Cali')
        g.insertVertex (graph, 'Medellin')
        g.insertVertex (graph, 'Pasto')
        g.insertVertex (graph, 'Barranquilla')
        g.insertVertex (graph, 'Manizales')


    def test_addEdges (self):
        graph = g.newGraph(7,self.comparenames)

        g.insertVertex (graph, 'Bogota')
        g.insertVertex (graph, 'Yopal')
        g.insertVertex (graph, 'Cali')
        g.insertVertex (graph, 'Medellin')
        g.insertVertex (graph, 'Pasto')
        g.insertVertex (graph, 'Barranquilla')
        g.insertVertex (graph, 'Manizales')

        g.addEdge (graph, 'Bogota', 'Yopal')
        g.addEdge (graph, 'Bogota', 'Medellin')
        g.addEdge (graph, 'Bogota', 'Pasto')
        g.addEdge (graph, 'Bogota', 'Cali')
        g.addEdge (graph, 'Yopal', 'Medellin')
        g.addEdge (graph, 'Medellin', 'Pasto')
        g.addEdge (graph, 'Cali', 'Pasto')
        g.addEdge (graph, 'Cali', 'Barranquilla')
        g.addEdge (graph, 'Barranquilla','Manizales')
        g.addEdge (graph, 'Pasto','Manizales')

        self.assertEqual (g.numEdges(graph), 10)
        self.assertEqual (g.numVertex(graph), 7)

        lst = g.vertices (graph)
        self.assertEqual (lt.size (lst), 7)

        lst = g.edges (graph)
        self.assertEqual (lt.size (lst), 10)

        degree = g.degree (graph, 'Bogota')
        self.assertEqual (degree, 4)

        edge = g.getEdge (graph, 'Bogota', 'Medellin')

        lst = g.adjacents (graph, 'Bogota')
        self.assertEqual (lt.size (lst), 4)

    def test_connectedcomponents (self):

        graph = g.newGraph(7,self.comparenames)

        g.insertVertex(graph, 'Laura')
        g.insertVertex(graph, 'Eduardo')
        g.insertVertex(graph, 'Andres')
        g.insertVertex(graph, 'Camila')
        g.insertVertex(graph, 'Antonio')
        g.insertVertex(graph, 'Luis')
        g.insertVertex(graph, 'Lina')

        g.addEdge(graph, 'Laura', 'Luis')
        g.addEdge(graph, 'Eduardo', 'Laura')
        g.addEdge(graph, 'Antonio', 'Laura')
        g.addEdge(graph, 'Camila', 'Lina')

        cc= dfs.countCC(graph)
        self.assertEqual (cc, 3)

    def test_dfs (self):
        graph = g.newGraph(7,self.comparenames)

        g.insertVertex (graph, 'Bogota')
        g.insertVertex (graph, 'Yopal')
        g.insertVertex (graph, 'Cali')
        g.insertVertex (graph, 'Medellin')
        g.insertVertex (graph, 'Pasto')
        g.insertVertex (graph, 'Barranquilla')
        g.insertVertex (graph, 'Manizales')

        g.addEdge (graph, 'Bogota', 'Yopal')
        g.addEdge (graph, 'Yopal', 'Cali')

        search= dfs.newDFS(graph, 'Bogota')
        response = ''
        path = dfs.pathTo(search, 'Cali')
        pathsize=0
        if path:
            iteraPath=it.newIterator(path)
            while it.hasNext(iteraPath):
                Vertex = it.next(iteraPath)
                response += Vertex +'\n'
                pathsize+=1
            print(response)
        self.assertEqual(pathsize, 3)

        path2 = dfs.pathTo(search, 'Pasto')
        self.assertIsNone(path2)

    def test_bfs(self):
        graph = g.newGraph(7,self.comparenames)

        g.insertVertex (graph, 'Bogota')
        g.insertVertex (graph, 'Yopal')
        g.insertVertex (graph, 'Cali')
        g.insertVertex (graph, 'Medellin')
        g.insertVertex (graph, 'Pasto')
        g.insertVertex (graph, 'Barranquilla')
        g.insertVertex (graph, 'Manizales')

        g.addEdge (graph, 'Bogota', 'Yopal')
        g.addEdge (graph, 'Yopal', 'Barranquilla')
        g.addEdge(graph, 'Barranquilla', 'Medellin')
        g.addEdge (graph, 'Bogota', 'Cali')
        g.addEdge (graph, 'Cali', 'Medellin')

        search= bfs.newBFS(graph, 'Bogota')
        response = ''
        path = bfs.pathTo(search, 'Medellin')
        pathsize=0
        if path:
            iteraPath=it.newIterator(path)
            while it.hasNext(iteraPath):
                Vertex = it.next(iteraPath)
                response += Vertex +'\n'
                pathsize+=1
            print(response)
        self.assertEqual(pathsize, 3)

        path2 = bfs.pathTo(search, 'Pasto')
        self.assertIsNone(path2)

if __name__ == "__main__":
    unittest.main()
