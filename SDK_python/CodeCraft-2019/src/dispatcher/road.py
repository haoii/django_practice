
from .car import CarStatus, Car


class HalfRoad:
    def __init__(self, id, length, max_v, lane_num, start, end, forward):
        self.id = id
        self.length = length
        self.max_v = max_v
        self.lane_num = lane_num
        self.start = start
        self.end = end
        self.forward = forward

        self.lanes = [[None] * length for _ in range(lane_num)]
        self.next_wait_car = None
        self.next_wait_car_pos = None
        self.next_wait_car_dist = None
        self.next_available_pos = (0, self.length-1)
        self.next_available_pos_stop = True

    def remove_car(self, pos):
        car = self.lanes[pos[0]][pos[1]]
        assert car
        self.lanes[pos[0]][pos[1]] = None
        return car

    def add_car(self, pos, car):
        assert not self.lanes[pos[0]][pos[1]]
        self.lanes[pos[0]][pos[1]] = car

    def _find_space(self, lane, i0):
        i = i0 + 1
        while i < self.length:
            if lane[i]:
                return i - i0 - 1, lane[i].status
            i += 1
        return i - i0 - 1, 'lane_end'

    def redispatch_step_one_a_lane(self, lane_i, complete_cars):
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
                        if car.is_last_path():
                            car.status = CarStatus.complete
                            car.go_next_road()
                            complete_cars.append(car)
                            lane[i] = None
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

    def dispatch_step_one(self, complete_cars):
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
                            if car.is_last_path():
                                car.status = CarStatus.complete
                                car.go_next_road()
                                complete_cars.append(car)
                                lane[i] = None
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
                    else:
                        lanes_to_remove.append(lane_i)
            [lanes_to_search.remove(i) for i in lanes_to_remove]
        self.next_wait_car = None
        self.next_wait_car_pos = None
        self.next_wait_car_dist = None

    def update_next_available_pos(self):
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
    def __init__(self, id, length, max_v, lane_num, start, end, both_way):
        self.id = id
        self.length = length
        self.max_v = max_v
        self.lane_num = lane_num
        self.start = start
        self.end = end
        self.both_way = both_way

        self.half_roads = [HalfRoad(id, length, max_v, lane_num, start, end, True)]
        if self.both_way:
            self.half_roads.append(HalfRoad(id, length, max_v, lane_num, end, start, False))

    def dispatch_step_one(self, complete_cars):
        for half_road in self.half_roads:
            half_road.dispatch_step_one(complete_cars)

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

    def __str__(self):
        return '道路' + str(self.id) + \
               '-长度' + str(self.length) + \
               '-限速' + str(self.max_v) + \
               '-车道数' + str(self.lane_num) + \
               '-起点' + str(self.start) + \
               '-终点' + str(self.end) + \
               '-双向' + str(self.both_way)



