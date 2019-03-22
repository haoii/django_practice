
import pprint
from short_path import DirectedEdge, EdgeWeightedDigraph, DijkstraSP


class Road:
    def __init__(self, id, length, max_v, lane_num, start, end, both_way):
        self.id = id
        self.length = length
        self.max_v = max_v
        self.lane_num = lane_num
        self.start = start
        self.end = end
        self.both_way = both_way

    def __str__(self):
        return '道路' + str(self.id) + \
               '-长度' + str(self.length) + \
               '-限速' + str(self.max_v) + \
               '-车道数' + str(self.lane_num) + \
               '-起点' + str(self.start) + \
               '-终点' + str(self.end) + \
               '-双向' + str(self.both_way)


class Cross:
    def __init__(self, id, road1, road2, road3, road4):
        self.id = id
        self.road1 = road1
        self.road2 = road2
        self.road3 = road3
        self.road4 = road4

    def __str__(self):
        return '路口' + str(self.id) + \
               '-道路' + str(self.road1) + \
               '-道路' + str(self.road2) + \
               '-道路' + str(self.road3) + \
               '-道路' + str(self.road4)


class Car:
    def __init__(self, id, start, end, max_v, planned_time):
        self.id = id
        self.start = start
        self.end = end
        self.max_v = max_v
        self.planned_time = planned_time

    def __str__(self):
        return '车辆' + str(self.id) + \
               '-起点' + str(self.start) + \
               '-终点' + str(self.end) + \
               '-限速' + str(self.max_v) + \
               '-计划出发时间' + str(self.planned_time)


class Dispatcher:
    def __init__(self, car_path, road_path, cross_path, answer_path):
        self.crosses = self.read_param_file(cross_path, Cross)
        self.roads = self.read_param_file(road_path, Road)
        self.cars = self.read_param_file(car_path, Car)

        # for r in self.roads:
        #     print(r)
        # for c in self.crosses:
        #     print(c)
        # for c in self.cars:
        #     print(c)

        cross_map = [c.id for c in self.crosses]
        for c in self.crosses:
            c.id = cross_map.index(c.id)
        for r in self.roads:
            r.start = cross_map.index(r.start)
            r.end = cross_map.index(r.end)
        for c in self.cars:
            c.start = cross_map.index(c.start)
            c.end = cross_map.index(c.end)

        graph = EdgeWeightedDigraph()
        for r in self.roads:
            graph.add_edge(DirectedEdge(r.start, r.end, r.id, r.length, r.max_v))
            if r.both_way:
                graph.add_edge(DirectedEdge(r.end, r.start, r.id, r.length, r.max_v))

        # paths = []
        # for c in self.cars:
        #     sp = DijkstraSP(graph, c.start, c.max_v)
        #     path = sp.path_to(c.end)
        #     paths.append('(' + str(c.id) + ',' + str(c.planned_time) + ',' + ','.join([str(p.id) for p in path]) + ')')

        paths = []
        t = 0
        while self.cars:
            t += 1
            for c in self.cars:
                if c.planned_time <= t:
                    sp = DijkstraSP(graph, c.start, c.max_v)
                    path = sp.path_to(c.end)
                    paths.append('(' + str(c.id) + ',' + str(t) + ',' + ','.join([str(p.id) for p in path]) + ')')
                    self.cars.remove(c)
                    break

        with open(answer_path, 'w') as f:
            f.writelines('\n'.join(paths))

    @staticmethod
    def read_param_file(path, cls):
        objects = []
        with open(path) as f:
            for line in f.readlines():
                line = line.strip()
                if line[0] != '#':
                    objects.append(cls(*[int(i) for i in line[1:-1].split(',')]))
        return objects

