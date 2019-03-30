
from .car import CarStatus, Car


class HalfRoad:
    def __init__(self, all_data, road, id, length, max_v, lane_num, start, end, forward):
        self.id = id
        self.length = length
        self.max_v = max_v
        self.lane_num = lane_num
        self.start = start
        self.end = end
        self.forward = forward
        self.road = road
        self.all_data = all_data

        self.tmp_hide = False

        self.car_num = 0
        self.lanes = [[None] * length for _ in range(lane_num)]
        self.next_wait_car = None
        self.next_wait_car_pos = None
        self.next_wait_car_dist = None
        self.next_available_pos = (0, self.length-1)
        self.next_available_pos_stop = True

        self.jam_num = 0
        self.use_degree = 0

    def hide_reverse_half_road(self):
        reverse_half_road = self.get_reverse_half_road()
        if reverse_half_road:
            reverse_half_road.tmp_hide = True

    def show_reverse_half_road(self):
        reverse_half_road = self.get_reverse_half_road()
        if reverse_half_road:
            reverse_half_road.tmp_hide = False

    def get_reverse_half_road(self):
        if self.forward:
            if self.road.both_way:
                return self.road.half_roads[1]
            else:
                return None
        else:
            return self.road.half_roads[0]

    def get_fill_rate(self):
        rate = self.car_num / (self.lane_num * self.length)
        return rate

    # def get_fill_rate(self):
    #     # rate = self.car_num / (self.lane_num * self.length)
    #
    #     around_pos, around_car_num = 0, 0
    #     enter_cross = self.all_data.crosses[self.start]
    #     quit_cross = self.all_data.crosses[self.end]
    #     for enter_road_id in enter_cross.road_ids:
    #         if enter_road_id > -1:
    #             enter_half_road = self.all_data.roads[enter_road_id].get_half_road_by_direct(self.start)
    #             if enter_half_road:
    #                 around_pos += enter_half_road.length * enter_half_road.lane_num
    #                 around_car_num += enter_half_road.car_num
    #     for quit_road_id in quit_cross.road_ids:
    #         if quit_road_id > -1:
    #             quit_half_road = self.all_data.roads[quit_road_id].get_half_road_by_start(self.end)
    #             if quit_half_road:
    #                 around_pos += quit_half_road.length * enter_half_road.lane_num
    #                 around_car_num += quit_half_road.car_num
    #
    #     return (self.car_num + around_car_num / 8) / (self.lane_num * self.length + around_pos / 8)

    def remove_car(self, pos):
        car = self.lanes[pos[0]][pos[1]]
        assert car
        self.lanes[pos[0]][pos[1]] = None
        self.car_num -= 1
        return car

    def add_car(self, pos, car):
        assert not self.lanes[pos[0]][pos[1]]
        self.lanes[pos[0]][pos[1]] = car
        self.car_num += 1

    def _find_space(self, lane, i0):
        i = i0 + 1
        while i < self.length:
            if lane[i]:
                return i - i0 - 1, lane[i].status
            i += 1
        return i - i0 - 1, 'lane_end'

    def redispatch_step_one_a_lane(self, lane_i):
        lane = self.lanes[lane_i]
        for i in range(self.length - 2, -1, -1):
            if lane[i]:
                car = lane[i]
                if car.status == CarStatus.stop:
                    break
                max_v = min(car.max_v, self.max_v)
                space, status = self._find_space(lane, i)
                if status == 'lane_end':
                    if space >= max_v:
                        lane[i], lane[i+max_v] = lane[i+max_v], lane[i]
                        car.status = CarStatus.stop
                    else:
                        assert car.status == CarStatus.wait
                        break
                elif status == CarStatus.stop:
                    move_space = min(space, max_v)
                    lane[i], lane[i+move_space] = lane[i+move_space], lane[i]
                    car.status = CarStatus.stop
                else:
                    assert False
        self.update_next_wait_car()
        self.update_next_available_pos()

    def dispatch_step_one(self):
        for lane in self.lanes:
            for i in range(self.length - 1, -1, -1):
                if lane[i]:
                    car = lane[i]
                    max_v = min(car.max_v, self.max_v)
                    space, status = self._find_space(lane, i)
                    if status == 'lane_end':
                        if space >= max_v:
                            lane[i], lane[i+max_v] = lane[i+max_v], lane[i]
                            car.status = CarStatus.stop
                        else:
                            car.status = CarStatus.wait
                    elif status == CarStatus.wait:
                        if space >= max_v:
                            lane[i], lane[i+max_v] = lane[i+max_v], lane[i]
                            car.status = CarStatus.stop
                        else:
                            car.status = CarStatus.wait
                    elif status == CarStatus.stop:
                        move_space = min(space, max_v)
                        lane[i], lane[i+move_space] = lane[i+move_space], lane[i]
                        car.status = CarStatus.stop
                    else:
                        assert False
        self.update_next_wait_car()
        self.update_next_available_pos()

    # def redispatch_step_one_a_lane(self, lane_i, complete_cars):
    #     lane = self.lanes[lane_i]
    #     for i in range(self.length - 2, -1, -1):
    #         if lane[i]:
    #             car = lane[i]
    #             if car.status == CarStatus.stop:
    #                 break
    #             max_v = min(car.max_v, self.max_v)
    #             space, status = self._find_space(lane, i)
    #             if status == 'lane_end':
    #                 if space > max_v or (not car.is_last_path() and space == max_v):
    #                     lane[i], lane[i+max_v] = lane[i+max_v], lane[i]
    #                     car.status = CarStatus.stop
    #                 elif space <= max_v and car.is_last_path():
    #                     car.status = CarStatus.complete
    #                     car.go_next_road()
    #                     complete_cars.append(car)
    #                     self.car_num -= 1
    #                     lane[i] = None
    #                 else:
    #                     assert car.status == CarStatus.wait
    #                     break
    #             elif status == CarStatus.stop:
    #                 move_space = min(space, max_v)
    #                 lane[i], lane[i+move_space] = lane[i+move_space], lane[i]
    #                 car.status = CarStatus.stop
    #             else:
    #                 assert False
    #     self.update_next_wait_car()
    #     self.update_next_available_pos()
    #
    # def dispatch_step_one(self, complete_cars):
    #     for lane in self.lanes:
    #         for i in range(self.length - 1, -1, -1):
    #             if lane[i]:
    #                 car = lane[i]
    #                 max_v = min(car.max_v, self.max_v)
    #                 space, status = self._find_space(lane, i)
    #                 if status == 'lane_end':
    #                     if space > max_v or (not car.is_last_path() and space == max_v):
    #                         lane[i], lane[i+max_v] = lane[i+max_v], lane[i]
    #                         car.status = CarStatus.stop
    #                     elif space <= max_v and car.is_last_path():
    #                         car.status = CarStatus.complete
    #                         car.go_next_road()
    #                         complete_cars.append(car)
    #                         self.car_num -= 1
    #                         lane[i] = None
    #                     else:
    #                         car.status = CarStatus.wait
    #                 elif status == CarStatus.wait:
    #                     if space >= max_v:
    #                         lane[i], lane[i+max_v] = lane[i+max_v], lane[i]
    #                         car.status = CarStatus.stop
    #                     else:
    #                         car.status = CarStatus.wait
    #                 elif status == CarStatus.stop:
    #                     move_space = min(space, max_v)
    #                     lane[i], lane[i+move_space] = lane[i+move_space], lane[i]
    #                     car.status = CarStatus.stop
    #                 else:
    #                     assert False
    #     self.update_next_wait_car()
    #     self.update_next_available_pos()

    def update_next_wait_car(self):
        lanes_to_search = list(range(self.lane_num))
        for pos_i in range(self.length-1, -1, -1):
            if not lanes_to_search:
                break
            lanes_to_remove = []
            for lane_i in lanes_to_search:
                if self.lanes[lane_i][pos_i]:
                    car = self.lanes[lane_i][pos_i]
                    if car.status == CarStatus.wait:
                        self.next_wait_car_pos = (lane_i, pos_i)
                        self.next_wait_car = car
                        self.next_wait_car_dist = self.length - pos_i - 1
                        return
                    elif car.status == CarStatus.stop:
                        lanes_to_remove.append(lane_i)
                    else:
                        assert False
            [lanes_to_search.remove(i) for i in lanes_to_remove]
        self.next_wait_car = None
        self.next_wait_car_pos = None
        self.next_wait_car_dist = None

    def update_next_available_pos(self):
        self.jam_num = 0
        for lane in self.lanes:
            if lane[0]:
                self.jam_num += 1

        for lane_i in range(self.lane_num):
            car0 = self.lanes[lane_i][0]
            if car0 and car0.status == CarStatus.stop:
                continue
            for pos_i in range(self.length):
                if self.lanes[lane_i][pos_i]:
                    self.next_available_pos = (lane_i, pos_i - 1)
                    self.next_available_pos_stop = self.lanes[lane_i][pos_i].status == CarStatus.stop
                    return
            self.next_available_pos = (lane_i, self.length - 1)
            self.next_available_pos_stop = True
            return
        self.next_available_pos = (0, -1)
        self.next_available_pos_stop = True

    def get_next_wait_car(self):
        return self.next_wait_car, \
               self.next_wait_car_dist, \
               self.next_wait_car_pos

    def get_next_available_pos(self):
        return self.next_available_pos, self.next_available_pos_stop

    def __str__(self):
        if self.forward:
            s = '道路{}的正向路({})：\n'.format(self.id, self.max_v)
        else:
            s = '道路{}的逆向路({})：\n'.format(self.id, self.max_v)
        for lane in self.lanes:
            for pos in lane:
                if pos:
                    s += str(pos.max_v)
                else:
                    s += '*'
            s += '\n'
        return s


class Road:
    def __init__(self, all_data, id, length, max_v, lane_num, start, end, both_way):
        self.id = id
        self.length = length
        self.max_v = max_v
        self.lane_num = lane_num
        self.start = start
        self.end = end
        self.both_way = both_way

        self.half_roads = [HalfRoad(all_data, self, id, length, max_v, lane_num, start, end, True)]
        if self.both_way:
            self.half_roads.append(HalfRoad(all_data, self, id, length, max_v, lane_num, end, start, False))

    def dispatch_step_one(self):
        for half_road in self.half_roads:
            half_road.dispatch_step_one()

    def get_half_road_by_direct(self, direct):
        if direct == self.end:
            return self.half_roads[0]
        elif direct == self.start:
            if not self.both_way:
                return None
            return self.half_roads[1]
        else:
            assert False

    def get_half_road_by_start(self, start):
        if start == self.start:
            return self.half_roads[0]
        elif start == self.end:
            if not self.both_way:
                return None
            return self.half_roads[1]
        else:
            assert False

    # def __str__(self):
    #     return '道路' + str(self.id) + \
    #            '-长度' + str(self.length) + \
    #            '-限速' + str(self.max_v) + \
    #            '-车道数' + str(self.lane_num) + \
    #            '-起点' + str(self.start) + \
    #            '-终点' + str(self.end) + \
    #            '-双向' + str(self.both_way)

    def __str__(self):
        s = '正向路：\n'
        for lane in self.half_roads[0].lanes:
            for pos in lane:
                if pos:
                    s += str(pos.max_v)
                else:
                    s += '_'
            s += '\n'

        placeholder = 120 - (len(s) + self.lane_num)
        if placeholder > 0:
            s += ' ' * placeholder

        if self.both_way:
            s += '逆向路：\n'
            for lane in self.half_roads[1].lanes:
                for pos in lane:
                    if pos:
                        s += str(pos.max_v)
                    else:
                        s += '_'
                s += '\n'

        return s




