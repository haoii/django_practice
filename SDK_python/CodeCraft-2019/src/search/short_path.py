
from collections import defaultdict
from .index_minPQ import IndexMinPQ

INFINITE_POSITIVE_NUMBER = float('inf')
INFINITE_NEGATIVE_NUMBER = float('-inf')


class DirectedEdge(object):

    def __init__(self, start, end, id, half_road):
        self.start = start
        self.end = end
        self.id = id
        self.half_road = half_road

    def weight(self, v):
        if self.half_road.tmp_hide:
            return 100000000
        duration0 = self.half_road.length / min(v, self.half_road.max_v)
        fill_rate = self.half_road.get_fill_rate()
        jam_rate = self.half_road.jam_num / self.half_road.lane_num
        use_degree = self.half_road.use_degree / 300

        # if jam_rate < 0.3:
        #     duration0 = duration0
        # elif jam_rate < 0.6:
        #     duration0 = (jam_rate - 0.3) * 8 + 1
        # else:
        #     duration0 = (jam_rate - 0.6) * 15 + 3.4

        # duration0 *= use_degree + 1

        if fill_rate < 0.3:
            return duration0
        elif fill_rate < 0.6:
            return ((fill_rate - 0.3) * 1.8 + 1) * duration0
        else:
            return ((fill_rate - 0.6) * 4.4 + 1.54) * duration0

        # if fill_rate < 0.3:
        #     return int(duration0) + 1
        # elif fill_rate < 0.6:
        #     return int(((fill_rate - 0.3) * 2 + 1) * duration0) + 1
        # else:
        #     return int(((fill_rate - 0.6) * 5 + 1.6) * duration0) + 1

        # if fill_rate < 0.4:
        #     return int(duration0) + 1
        # elif fill_rate < 0.7:
        #     return int(((fill_rate - 0.4) * 1.6 + 1) * duration0) + 1
        # else:
        #     return int(((fill_rate - 0.7) * 3.5 + 1.48) * duration0) + 1

        # if fill_rate < 0.1:
        #     return int(duration0) + 1
        # elif fill_rate < 0.3:
        #     return int(((fill_rate - 0.1) * 5 + 1) * duration0) + 1
        # elif fill_rate < 0.5:
        #     return int(((fill_rate - 0.3) * 10 + 2) * duration0) + 1
        # elif fill_rate < 0.7:
        #     return int(((fill_rate - 0.5) * 20 + 4) * duration0) + 1
        # else:
        #     return int(((fill_rate - 0.7) * 40 + 8) * duration0) + 1

        # if jam_rate < 0.3:
        #     duration0 += jam_rate * 10
        # elif jam_rate < 0.6:
        #     duration0 += (jam_rate - 0.3) * 12 + 3
        # else:
        #     duration0 = (jam_rate - 0.6) * 30 + 6.6
        #
        # if fill_rate < 0.3:
        #     duration0 += fill_rate * 10
        # elif fill_rate < 0.6:
        #     duration0 += (fill_rate - 0.3) * 12 + 3
        # else:
        #     duration0 = (fill_rate - 0.6) * 30 + 6.6
        #
        # return int(duration0) + 1

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

    def __init__(self, graph, source, end, car_v):
        self._dist_to = dict((v, INFINITE_POSITIVE_NUMBER) for v in graph.vertices())
        self._edge_to = {}
        self._pq = IndexMinPQ(graph.vertices_size())
        self._pq.insert(source, 0)
        self._edge_to[source] = None
        self._dist_to[source] = 0
        self.end = end

        while not self._pq.is_empty():
            vertex = self._pq.delete_min()
            if vertex == self.end:
                break
            for edge in graph.adjacent_edges(vertex):
                end = edge.end
                if self._dist_to[end] > self._dist_to[vertex] + edge.weight(car_v):
                    self._dist_to[end] = self._dist_to[vertex] + edge.weight(car_v)
                    self._edge_to[end] = edge

                    if self._pq.contains(end):
                        self._pq.change_key(end, self._dist_to[end])
                    else:
                        self._pq.insert(end, self._dist_to[end])

    #     while not self._pq.is_empty():
    #         self.relax(graph, self._pq.delete_min(), car_v)
    #
    # def relax(self, graph, vertex, car_v):
    #     for edge in graph.adjacent_edges(vertex):
    #         end = edge.end
    #         if self._dist_to[end] > self._dist_to[vertex] + edge.weight(car_v):
    #             self._dist_to[end] = self._dist_to[vertex] + edge.weight(car_v)
    #             self._edge_to[end] = edge
    #
    #             if self._pq.contains(end):
    #                 self._pq.change_key(end, self._dist_to[end])
    #             else:
    #                 self._pq.insert(end, self._dist_to[end])

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

        # path_dict = {'c' + str(path[0].end): 'end'}
        # for p in path:
        #     path_dict['r' + str(p.id)] = 'c' + str(p.end)
        #     path_dict['c' + str(p.start)] = 'r' + str(p.id)
        # path_dict['start'] = 'c' + str(path[-1].start)
        #
        # return reversed(path), path_dict

        return path[-1].half_road

    def get_path(self, vertex):
        if not self.has_path_to(vertex):
            return None
        path = []
        edge = self._edge_to[vertex]
        while edge:
            path.append(edge)
            edge = self._edge_to[edge.start]
        return reversed(path)
