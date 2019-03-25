
from .car import CarStatus, Car


class Dispatcher:
    def __init__(self, roads, crosses, cars_to_run, cars_run, cars_complete):
        self.roads = roads
        self.crosses = crosses
        self.cars_to_run = cars_to_run
        self.cars_run = cars_run
        self.cars_complete = cars_complete

    def is_all_car_stop(self):
        for _, c in self.cars_run.items():
            if c.status != CarStatus.stop:
                return False
        return True

    def dispatch(self, t):
        # self.cars.clear()

        for _, car in self.cars_run.items():
            car.status = CarStatus.init

        for _, road in self.roads.items():
            complete_cars = []
            road.dispatch_step_one(complete_cars)
            for car in complete_cars:
                del self.cars_run[car.id]
                self.cars_complete[car.id] = car

        dispatch_turns = 0
        while not self.is_all_car_stop():
            dispatch_turns += 1
            if dispatch_turns > 100:
                assert False

            for cross_id in range(len(self.crosses)):
                cross = self.crosses[cross_id]
                id_ordered_road_ids = cross.id_ordered_road_ids()

                dispatched_this_cross = True
                while dispatched_this_cross:
                    dispatched_this_cross = False

                    for road_id in id_ordered_road_ids:
                        if road_id < 0:
                            continue
                        half_road = self.roads[road_id].get_half_road_by_direct(cross_id)
                        if not half_road:
                            continue

                        while True:
                            next_wait_car, next_wait_car_dist, next_wait_car_pos = \
                                half_road.get_next_wait_car()
                            if not next_wait_car:
                                break
                            next_road_id = next_wait_car.get_next_road_id()
                            next_half_road = self.roads[next_road_id].get_half_road_by_start(cross_id)
                            if not next_half_road:
                                assert False
                            next_available_pos, next_available_pos_stop = next_half_road.get_next_available_pos()
                            next_max_v = min(next_wait_car.max_v, next_half_road.max_v)
                            if not next_available_pos_stop:
                                if next_max_v > next_wait_car_dist and \
                                        next_available_pos[1] + 1 < next_max_v - next_wait_car_dist:
                                    break

                            next_wait_car_direct = cross.get_direct(road_id, next_road_id)
                            if next_wait_car_direct == 'D':
                                self._dispatch_between_two_half_roads(
                                    half_road, next_wait_car, next_wait_car_dist,
                                    next_wait_car_pos, next_half_road, next_available_pos, next_max_v)
                                dispatched_this_cross = True

                            elif next_wait_car_direct == 'L':
                                d_road_id = cross.get_road_id_by_direct(road_id, 'R')
                                if self._get_wait_car_direct_by_road_id(cross_id, cross, d_road_id) == 'D':
                                    break

                                self._dispatch_between_two_half_roads(
                                    half_road, next_wait_car, next_wait_car_dist,
                                    next_wait_car_pos, next_half_road, next_available_pos, next_max_v)
                                dispatched_this_cross = True

                            elif next_wait_car_direct == 'R':
                                d_road_id = cross.get_road_id_by_direct(road_id, 'L')
                                if self._get_wait_car_direct_by_road_id(cross_id, cross, d_road_id) == 'D':
                                    break
                                l_road_id = cross.get_road_id_by_direct(road_id, 'D')
                                if self._get_wait_car_direct_by_road_id(cross_id, cross, l_road_id) == 'L':
                                    break

                                self._dispatch_between_two_half_roads(
                                    half_road, next_wait_car, next_wait_car_dist,
                                    next_wait_car_pos, next_half_road, next_available_pos, next_max_v)
                                dispatched_this_cross = True

        start_ts = sorted(self.cars_to_run.keys())
        cars_has_run = {}
        for start_t in start_ts:
            if start_t > t:
                break
            cars_before_t = self.cars_to_run[start_t]
            car_ids = sorted(cars_before_t.keys())
            for car_id in car_ids:
                car = cars_before_t[car_id]
                next_road_id = car.get_next_road_id()
                next_half_road = self.roads[next_road_id].get_half_road_by_start(car.get_start_cross_id())
                if not next_half_road:
                    assert False
                next_available_pos, next_available_pos_stop = next_half_road.get_next_available_pos()
                assert next_available_pos_stop
                if next_available_pos[1] < 0:
                    break

                new_move_dist = min(car.max_v, next_half_road.max_v, next_available_pos[1] + 1)
                next_half_road.add_car((next_available_pos[0], new_move_dist - 1), car)
                car.go_next_road()
                car.status = CarStatus.stop
                next_half_road.update_next_available_pos()

                if start_t not in cars_has_run:
                    cars_has_run[start_t] = []
                cars_has_run[start_t].append(car_id)

        for start_t, car_ids in cars_has_run.items():
            for car_id in car_ids:
                car = self.cars_to_run[start_t][car_id]
                self.cars_run[car.id] = car
                del self.cars_to_run[start_t][car_id]
            if not self.cars_to_run[start_t]:
                del self.cars_to_run[start_t]

    def _get_wait_car_direct_by_road_id(self, cross_id, cross, road_id):
        if road_id != -1:
            half_road = self.roads[road_id].get_half_road_by_direct(cross_id)
            if half_road:
                next_wait_car, _, _ = half_road.get_next_wait_car()
                if next_wait_car:
                    next_road_id = next_wait_car.get_next_road_id()
                    return cross.get_direct(road_id, next_road_id)

    def _dispatch_between_two_half_roads(self, half_road, next_wait_car, next_wait_car_dist,
                                         next_wait_car_pos, next_half_road, next_available_pos, next_max_v):
        # 调度此车到另一车道
        if next_max_v <= next_wait_car_dist or next_available_pos[1] < 0:
            new_pos = (next_wait_car_pos[0], next_wait_car_pos[1] + next_wait_car_dist)
            half_road.add_car(new_pos, half_road.remove_car(next_wait_car_pos))
        else:
            new_move_dist = min(next_max_v - next_wait_car_dist,
                                next_available_pos[1] + 1)
            next_half_road.add_car((next_available_pos[0], new_move_dist - 1),
                                   half_road.remove_car(next_wait_car_pos))
            next_wait_car.go_next_road()
        next_wait_car.status = CarStatus.stop

        # 内部调度上一车道
        complete_cars = []
        half_road.redispatch_step_one_a_lane(next_wait_car_pos[0], complete_cars)
        for car in complete_cars:
            del self.cars_run[car.id]
            self.cars_complete[car.id] = car

        # 更新下车道状态
        next_half_road.update_next_available_pos()


