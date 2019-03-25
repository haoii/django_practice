
from .short_path import EdgeWeightedDigraph, DijkstraSP, DirectedEdge


class Searcher:
    def __init__(self, answer_path, dispatcher, roads, cars, cars_to_run):
        self.answer_path = answer_path
        self.dispatcher = dispatcher
        self.roads = roads
        self.cars_to_run = cars_to_run
        self.cars = cars

        self.graph = EdgeWeightedDigraph()
        for _, r in self.roads.items():
            self.graph.add_edge(DirectedEdge(r.start, r.end, r.id, r.half_roads[0]))
            if r.both_way:
                self.graph.add_edge(DirectedEdge(r.end, r.start, r.id, r.half_roads[1]))

    def open_loop_to_find_paths(self):
        cars_copy = self.cars.copy()
        paths = []
        t = 0
        while cars_copy:
            t += 1
            start_num = 0
            start_ids = []
            for key, c in cars_copy.items():
                if c.planned_time <= t:
                    sp = DijkstraSP(self.graph, c.start, c.max_v)
                    path, path_dict = sp.path_to(c.end)
                    paths.append('(' + str(c.id) + ',' + str(t) + ','
                                 + ','.join([str(p.id) for p in path]) + ')')
                    c.path = path_dict
                    c.start_t = t
                    start_ids.append(key)
                    start_num += 1
                    if start_num == 10:
                        break
            for key in start_ids:
                del cars_copy[key]

        with open(self.answer_path, 'w') as f:
            f.writelines('\n'.join(paths))

        for _, c in self.cars.items():
            if c.start_t in self.cars_to_run:
                self.cars_to_run[c.start_t][c.id] = c
            else:
                self.cars_to_run[c.start_t] = {c.id: c}
        self.cars.clear()

    def search(self, t):
        start_num = 0
        start_ids = []
        for key, c in self.cars.items():
            if c.planned_time <= t:
                sp = DijkstraSP(self.graph, c.start, c.max_v)
                path, path_dict = sp.path_to(c.end)
                c.path_str = '(' + str(c.id) + ',' + str(t) + ',' + ','.join([str(p.id) for p in path]) + ')'
                c.path = path_dict
                c.start_t = t
                start_ids.append(key)
                start_num += 1
                if start_num == 10:
                    break
        for key in start_ids:
            car = self.cars[key] 
            if car.start_t in self.cars_to_run:
                self.cars_to_run[car.start_t][car.id] = car
            else:
                self.cars_to_run[car.start_t] = {car.id: car}
            del self.cars[key]
