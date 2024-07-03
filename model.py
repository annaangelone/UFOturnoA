import copy

from database.DAO import DAO
from geopy.distance import geodesic
import networkx as nx
class Model:
    def __init__(self):
        self._shapes = []
        self._states = DAO.getStates()
        self._idMap = {}
        for s in self._states:
            self._idMap[s.id] = s

        self._grafo = nx.Graph()
        self._bestPath = []
        self._bestObj = 0


    def getShapes(self, year):
        self._shapes = DAO.getShapes(year)
        return self._shapes

    def getPeso(self, n1, n2):
        return self._grafo[n1][n2]["weight"]


    def buildGraph(self, year, shape):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._states)

        for u in self._grafo.nodes:
            for v in self._grafo.nodes:
                if u != v:
                    peso = DAO.getPeso(u.id, v.id, shape, year)
                    if (DAO.getEdges(u.id, v.id)):
                        self._grafo.add_edge(u, v, weight=0)

                        if peso:
                            self._grafo[u][v]["weight"] = peso[0]


    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def stampaPesiAdiacenti(self):
        pesiVicini = {}
        for s in self._states:
            vicini = self._grafo.neighbors(s)

            pesoTot = 0

            for v in vicini:
                pesoTot += self._grafo[s][v]["weight"]

            pesiVicini[s] = pesoTot

        return pesiVicini


    def getPercorso(self):
        self._bestPath = []
        self._bestObj = 0

        for nodo in self._grafo.nodes:
            parziale = [nodo]

            vicini = []
            for v in self._grafo.neighbors(nodo):
                vicini.append((v, self.getPeso(nodo, v)))

            if len(vicini) > 0:
                vicini.sort(key=lambda x: x[1])
                parziale.append(vicini[0][0])
                self._ricorsione(parziale)

        return self._bestPath, self._bestObj


    def _ricorsione(self, parziale):

        if self.getDistanzaTotale(parziale) > self._bestObj:
            self._bestObj = self.getDistanzaTotale(parziale)
            self._bestPath = copy.deepcopy(parziale)

        vicini = []

        for v in self._grafo.neighbors(parziale[-1]):
            vicini.append((v, self.getPeso(parziale[-1], v)))

        vicini.sort(key=lambda x:x[1])

        for v in vicini:
            if v[1] > self.getPeso(parziale[-2], parziale[-1]):
                parziale.append(v[0])
                self._ricorsione(parziale)
                parziale.pop()



    def getDistanzaTotale(self, parziale):
        distanzaTotale = 0

        for i in range(len(parziale) - 1):
            distanzaTotale += self.getDistanza(parziale[i], parziale[i+1])

        return distanzaTotale



    def getDistanza(self, nodo1, nodo2):
        distanzaNodi = geodesic((nodo1.Lat, nodo1.Lng), (nodo2.Lat, nodo2.Lng)).kilometers
        return distanzaNodi
