
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
        if self.all_data.running_pace < 12:
            max_fill_rate = 0.28
        else:
            max_fill_rate = 0.24
        return int(self.all_data.total_road_pos * max_fill_rate) - len(self.all_data.cars_run)

    def search(self, t):
        if self.all_data.running_pace < 12:
            max_fill_num = 35
        else:
            max_fill_num = 20

        start_num = 0
        max_start_num = min(max_fill_num, self.get_max_start_num())
        # if 50 < t < 200:
        #     max_start_num = 30
        start_ids = []

        car_ids = sorted(self.all_data.cars.keys())
        for key in car_ids:
            car = self.all_data.cars[key]

            if car.planned_time <= t:
                sp = DijkstraSP(self.all_data.graph, car.start, car.end, car.max_v)
                new_r = sp.path_to(car.end)

                if new_r[0].get_fill_rate() > 0.3:
                    continue

                car.path = new_r[:2]

                car.start_t = t
                if car.path[-1].end == car.end:
                    car.path.append('end')

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
            if car.path[-1] != 'end' and car.cur_pos == len(car.path) - 1:
                car.path[-1].hide_reverse_half_road()
                sp = DijkstraSP(self.all_data.graph, car.path[-1].end, car.end, car.max_v)
                car.path[-1].show_reverse_half_road()
                new_r = sp.path_to(car.end)

                car.path += new_r[:4]
                if car.path[-1].end == car.end:
                    car.path.append('end')


