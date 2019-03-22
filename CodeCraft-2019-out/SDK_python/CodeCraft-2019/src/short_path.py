
import doctest
import pprint
from collections import defaultdict
from basic_data_struct import IndexMinPQ

INFINITE_POSITIVE_NUMBER = float('inf')
INFINITE_NEGATIVE_NUMBER = float('-inf')


class DirectedEdge(object):

    def __init__(self, start, end, id, length, max_v):
        self.start = start
        self.end = end
        self.id = id
        self.length = length
        self.max_v = max_v

    def weight(self, v):
        return self.length // min(v, self.max_v) + 1

    def __repr__(self):
        return '点{}->路{}->点{}'.format(self.start, self.id, self.end)


class EdgeWeightedDigraph(object):

    def __init__(self):
        self._vertices = set()
        self._edges_size = 0
        self._adj = defaultdict(list)

    def add_edge(self, edge):
        self._adj[edge.start].append(edge)
        self._vertices.add(edge.start)
        self._vertices.add(edge.end)
        self._edges_size += 1

    def adjacent_edges(self, vertex):
        return self._adj[vertex]

    def edges(self):
        result = []
        for v in self._vertices:
            for edge in self._adj[v]:
                result.append(edge)
        return result

    def vertices(self):
        return self._vertices

    def vertices_size(self):
        return len(self._vertices)

    def edges_size(self):
        return self._edges_size


class DijkstraSP:

    def __init__(self, graph, source, car_v):
        self._dist_to = dict((v, INFINITE_POSITIVE_NUMBER) for v in graph.vertices())
        self._edge_to = {}
        self._pq = IndexMinPQ(graph.vertices_size())
        self._pq.insert(source, 0)
        self._edge_to[source] = None
        self._dist_to[source] = 0

        while not self._pq.is_empty():
            self.relax(graph, self._pq.delete_min(), car_v)

    def relax(self, graph, vertex, car_v):
        for edge in graph.adjacent_edges(vertex):
            end = edge.end
            if self._dist_to[end] > self._dist_to[vertex] + edge.weight(car_v):
                self._dist_to[end] = self._dist_to[vertex] + edge.weight(car_v)
                self._edge_to[end] = edge

                if self._pq.contains(end):
                    self._pq.change_key(end, self._dist_to[end])
                else:
                    self._pq.insert(end, self._dist_to[end])

    def dist_to(self, vertex):
        return self._dist_to[vertex]

    def has_path_to(self, vertex):
        return self._dist_to[vertex] < INFINITE_POSITIVE_NUMBER

    def path_to(self, vertex):
        if not self.has_path_to(vertex):
            return None
        path = []
        edge = self._edge_to[vertex]
        while edge:
            path.append(edge)
            edge = self._edge_to[edge.start]
        return reversed(path)


if __name__ == '__main__':
    doctest.testmod()
