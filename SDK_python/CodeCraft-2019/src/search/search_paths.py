
from .short_path import EdgeWeightedDigraph, DijkstraSP, DirectedEdge


class Searcher:
    def __init__(self, all_data):
        self.all_data = all_data

    def open_loop_to_find_paths(self):
        cars_copy = self.all_data.cars.copy()
        paths = []
        t = 0
        while cars_copy:
            t += 1
            start_num = 0
            start_ids = []
            for key, c in cars_copy.items():
                if c.planned_time <= t:
                    sp = DijkstraSP(self.all_data.graph, c.start, c.max_v)
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

        # with open(self.answer_path, 'w') as f:
        #     f.writelines('\n'.join(paths))

        for _, c in self.all_data.cars.items():
            if c.start_t in self.all_data.cars_to_run:
                self.all_data.cars_to_run[c.start_t][c.id] = c
            else:
                self.all_data.cars_to_run[c.start_t] = {c.id: c}
        self.all_data.cars.clear()

    def get_max_start_num(self):
        return int(self.all_data.total_road_pos * 0.3) - len(self.all_data.cars_run)

    def search(self, t):
        start_num = 0
        max_start_num = min(40, self.get_max_start_num())
        # if 50 < t < 200:
        #     max_start_num = 30
        start_ids = []

        car_ids = sorted(self.all_data.cars.keys())
        for key in car_ids:
            car = self.all_data.cars[key]

            if car.planned_time <= t:
                sp = DijkstraSP(self.all_data.graph, car.start, car.end, car.max_v)
                new_r = sp.path_to(car.end)

                if new_r.get_fill_rate() > 0.3:
                    continue

                car.path = [new_r]

                car.start_t = t
                car.last_r = new_r
                if new_r.end == car.end:
                    car.path.append('end')
                    car.last_r = 'complete'

                start_ids.append(key)

                start_num += 1
                if start_num >= max_start_num:
                    break

        for key in start_ids:
            car = self.all_data.cars[key]
            if car.start_t in self.all_data.cars_to_run:
                self.all_data.cars_to_run[car.start_t][car.id] = car
            else:
                self.all_data.cars_to_run[car.start_t] = {car.id: car}
            del self.all_data.cars[key]

        for _, car in self.all_data.cars_run.items():
            if car.path[car.cur_pos] == car.last_r:
                car.last_r.hide_reverse_half_road()
                sp = DijkstraSP(self.all_data.graph, car.last_r.end, car.end, car.max_v)
                car.last_r.show_reverse_half_road()
                new_r = sp.path_to(car.end)

                car.path.append(new_r)
                car.last_r = new_r
                if new_r.end == car.end:
                    car.path.append('end')
                    car.last_r = 'complete'


