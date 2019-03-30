
import sys
import pickle

from dispatcher.dispatch import Dispatcher
from search.search_paths import Searcher
from dispatcher.road import Road
from dispatcher.cross import Cross
from dispatcher.car import Car
from search.short_path import EdgeWeightedDigraph, DirectedEdge, DijkstraSP

sys.setrecursionlimit(10000)


def read_param_file(path, cls, all_data):
    objects = {}
    with open(path) as f:
        for line in f.readlines():
            line = line.strip()
            if line[0] != '#':
                param = [int(i) for i in line[1:-1].split(',')]
                objects[param[0]] = cls(all_data, *[int(i) for i in line[1:-1].split(',')])
    return objects


class AllData:
    def __init__(self, car_path, road_path, cross_path):
        self.crosses = read_param_file(cross_path, Cross, self)
        self.roads = read_param_file(road_path, Road, self)
        self.cars = read_param_file(car_path, Car, self)

        cross_map = list(self.crosses.keys())
        cross_map.sort()
        crosses_tmp = {}
        for _, c in self.crosses.items():
            crosses_tmp[cross_map.index(c.id)] = c
            c.id = cross_map.index(c.id)
        self.crosses = crosses_tmp

        for _, r in self.roads.items():
            r.start = cross_map.index(r.start)
            r.end = cross_map.index(r.end)
            for half_r in r.half_roads:
                half_r.start = cross_map.index(half_r.start)
                half_r.end = cross_map.index(half_r.end)
        for _, c in self.cars.items():
            c.start = cross_map.index(c.start)
            c.end = cross_map.index(c.end)

        self.cars_to_run = {}
        self.cars_run = {}
        self.cars_complete = {}

        self.graph = EdgeWeightedDigraph()
        for _, r in self.roads.items():
            self.graph.add_edge(DirectedEdge(r.start, r.end, r.id, r.half_roads[0]))
            if r.both_way:
                self.graph.add_edge(DirectedEdge(r.end, r.start, r.id, r.half_roads[1]))

        self.total_car_num = len(self.cars)
        self.total_road_pos = 0
        for _, r in self.roads.items():
            for hf_r in r.half_roads:
                self.total_road_pos += hf_r.lane_num * hf_r.length

        self.dump_dat = None

    def dumps(self):
        self.dump_dat = pickle.dumps(
            (self.crosses, self.roads, self.cars, self.cars_to_run,
             self.cars_run, self.cars_complete, self.graph))

    def loads(self):
        (self.crosses, self.roads, self.cars, self.cars_to_run,
         self.cars_run, self.cars_complete, self.graph) = pickle.loads(self.dump_dat)


def entry(car_path, road_path, cross_path, answer_path):

    all_data = AllData(car_path, road_path, cross_path)

    dispatcher = Dispatcher(all_data)
    searcher = Searcher(all_data)

    # searcher.open_loop_to_find_paths()

    # for cross_id, cross in all_data.crosses.items():
    #     if cross.is_border:
    #         sp = DijkstraSP(all_data.graph, cross_id, 1000)
    #         for dist_cross_id, dist in sp._dist_to.items():
    #             if dist < all_data.crosses[dist_cross_id].dist_to_border:
    #                 all_data.crosses[dist_cross_id].dist_to_border = dist
    # for cross_id, cross in all_data.crosses.items():
    #     print('{}距离边缘:{}'.format(cross_id, cross.dist_to_border))
    #
    # return

    # for _, car in all_data.cars.items():
    #     sp = DijkstraSP(all_data.graph, car.start, car.max_v)
    #     path = sp.get_path(car.end)
    #     for edge in path:
    #         edge.half_road.use_degree += 1
    # for _, r in all_data.roads.items():
    #     for hf_r in r.half_roads:
    #         print('{}道路使用次数：{}'.format(hf_r.id, hf_r.use_degree))
    # return


    t = 0
    while all_data.cars or all_data.cars_to_run or all_data.cars_run:
        t += 1

        searcher.search(t)
        dispatch_turns = dispatcher.dispatch(t)

    #     print('time:{} complete:{} run:{} total:{} dispatch_turns:{}'.format(
    #         t, len(all_data.cars_complete), len(all_data.cars_run),
    #         all_data.total_car_num, dispatch_turns))
    #
    # print('调度时间：', t)
    # for _, c in cars_complete.items():
    #     print(c.path)

    with open(answer_path, 'w') as f:

        # write_paths = {}
        # for _, c in cars_complete.items():
        #     if c.start_t in write_paths:
        #         write_paths[c.start_t][c.id] = c.path_str
        #     else:
        #         write_paths[c.start_t] = {c.id: c.path_str}
        #
        # paths = []
        # start_ts = sorted(write_paths.keys())
        # for start_t in start_ts:
        #     start_tpath = write_paths[start_t]
        #     ids = sorted(start_tpath.keys())
        #     for id in ids:
        #         paths.append(start_tpath[id])

        paths = [c.get_path_str() for _, c in all_data.cars_complete.items()]
        f.writelines('\n'.join(paths))

