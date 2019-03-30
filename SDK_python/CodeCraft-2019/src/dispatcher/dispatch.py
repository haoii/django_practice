
from .car import CarStatus, Car


class Dispatcher:
    def __init__(self, all_data):
        self.all_data = all_data

    def is_all_car_stop(self):
        for _, c in self.all_data.cars_run.items():
            if c.status != CarStatus.stop:
                return False
        return True

    def dispatch(self, t):

        # self.all_data.dumps()
        # self.all_data.loads()

        for _, car in self.all_data.cars_run.items():
            car.status = CarStatus.init

        for _, road in self.all_data.roads.items():
            road.dispatch_step_one()

        dispatch_turns = 0
        dispatched_this_t = True
        is_all_car_stop = self.is_all_car_stop()
        while dispatched_this_t and not is_all_car_stop:
            dispatched_this_t = False
            dispatch_turns += 1
            if dispatch_turns > 100:
                assert False

        # dispatch_turns = 0
        # dispatched_this_t = True
        # is_all_car_stop = self.is_all_car_stop()
        # while not is_all_car_stop:
        #     dispatched_this_t = False
        #     dispatch_turns += 1
        #     if dispatch_turns > 100:
        #         assert False

            for cross_id in range(len(self.all_data.crosses)):
                cross = self.all_data.crosses[cross_id]
                id_ordered_road_ids = cross.id_ordered_road_ids()

                dispatched_this_cross = True
                while dispatched_this_cross:
                    dispatched_this_cross = False

                    for road_id in id_ordered_road_ids:
                        if road_id < 0:
                            continue
                        half_road = self.all_data.roads[road_id].get_half_road_by_direct(cross_id)
                        if not half_road:
                            continue

                        while True:
                            next_wait_car, next_wait_car_dist, next_wait_car_pos = \
                                half_road.get_next_wait_car()
                            if not next_wait_car:
                                break
                            next_road_id = next_wait_car.get_next_road_id()

                            if next_road_id == 'end':
                                tmp_stop_car = half_road.remove_car(next_wait_car_pos)
                                tmp_stop_car.status = CarStatus.complete
                                tmp_stop_car.go_next_road()
                                del self.all_data.cars_run[tmp_stop_car.id]
                                self.all_data.cars_complete[tmp_stop_car.id] = tmp_stop_car
                                half_road.redispatch_step_one_a_lane(next_wait_car_pos[0])
                                continue

                            next_half_road = self.all_data.roads[next_road_id].get_half_road_by_start(cross_id)
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
                                dispatched_this_t = True

                            elif next_wait_car_direct == 'L':
                                d_road_id = cross.get_road_id_by_direct(road_id, 'R')
                                if self._get_wait_car_direct_by_road_id(cross_id, cross, d_road_id) == 'D':
                                    break

                                self._dispatch_between_two_half_roads(
                                    half_road, next_wait_car, next_wait_car_dist,
                                    next_wait_car_pos, next_half_road, next_available_pos, next_max_v)
                                dispatched_this_cross = True
                                dispatched_this_t = True

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
                                dispatched_this_t = True

            is_all_car_stop = self.is_all_car_stop()

        if not is_all_car_stop:
            assert False
            assert not dispatched_this_t

            print('deadlock')

            wait_car_new_half_road = []

            for cross_id in range(len(self.all_data.crosses)):
                cross = self.all_data.crosses[cross_id]
                id_ordered_road_ids = cross.id_ordered_road_ids()

                for road_id in id_ordered_road_ids:
                    if road_id < 0:
                        continue
                    half_road = self.all_data.roads[road_id].get_half_road_by_direct(cross_id)
                    if not half_road:
                        continue

                    next_wait_car, next_wait_car_dist, next_wait_car_pos = \
                        half_road.get_next_wait_car()
                    if not next_wait_car:
                        continue

                    next_road_id = next_wait_car.get_next_road_id()
                    if next_road_id == 'end':
                        continue
                    next_half_road = self.all_data.roads[next_road_id].get_half_road_by_start(cross_id)
                    if not next_half_road:
                        assert False

                    next_wait_car_direct = cross.get_direct(road_id, next_road_id)
                    if next_wait_car_direct == 'D':
                        l_road_id = cross.get_road_id_by_direct(road_id, 'L')
                        if l_road_id != -1:
                            l_half_road = self.all_data.roads[l_road_id].get_half_road_by_start(cross_id)
                            if l_half_road:
                                wait_car_new_half_road.append((l_half_road.id, l_half_road.forward, next_wait_car.id))
                                break
                        r_road_id = cross.get_road_id_by_direct(road_id, 'R')
                        if r_road_id != -1:
                            r_half_road = self.all_data.roads[r_road_id].get_half_road_by_start(cross_id)
                            if r_half_road:
                                wait_car_new_half_road.append((r_half_road.id, r_half_road.forward, next_wait_car.id))
                                break

                    elif next_wait_car_direct == 'L':
                        d_road_id = cross.get_road_id_by_direct(road_id, 'D')
                        if d_road_id != -1:
                            d_half_road = self.all_data.roads[d_road_id].get_half_road_by_start(cross_id)
                            if d_half_road:
                                wait_car_new_half_road.append((d_half_road.id, d_half_road.forward, next_wait_car.id))
                                break
                        r_road_id = cross.get_road_id_by_direct(road_id, 'R')
                        if r_road_id != -1:
                            r_half_road = self.all_data.roads[r_road_id].get_half_road_by_start(cross_id)
                            if r_half_road:
                                wait_car_new_half_road.append((r_half_road.id, r_half_road.forward, next_wait_car.id))
                                break

                    elif next_wait_car_direct == 'R':
                        d_road_id = cross.get_road_id_by_direct(road_id, 'D')
                        if d_road_id != -1:
                            d_half_road = self.all_data.roads[d_road_id].get_half_road_by_start(cross_id)
                            if d_half_road:
                                wait_car_new_half_road.append((d_half_road.id, d_half_road.forward, next_wait_car.id))
                                break
                        l_road_id = cross.get_road_id_by_direct(road_id, 'L')
                        if l_road_id != -1:
                            l_half_road = self.all_data.roads[l_road_id].get_half_road_by_start(cross_id)
                            if l_half_road:
                                wait_car_new_half_road.append((l_half_road.id, l_half_road.forward, next_wait_car.id))
                                break

            self.all_data.loads()
            for i, change in enumerate(wait_car_new_half_road):
                if i % 2 == 0:
                    wait_car = self.all_data.cars_run[change[2]]
                    if change[1]:
                        new_half_road = self.all_data.roads[change[0]].half_roads[0]
                    else:
                        new_half_road = self.all_data.roads[change[0]].half_roads[1]
                    if wait_car.path[-1] == 'end':
                        del wait_car.path[-1]
                    wait_car.path[-1] = new_half_road
                    wait_car.last_r = new_half_road
                    if new_half_road.end == wait_car.end:
                        wait_car.path.append('end')
                        wait_car.last_r = 'complete'

            return self.dispatch(t)

        start_ts = sorted(self.all_data.cars_to_run.keys())
        cars_has_run = {}
        for start_t in start_ts:
            if start_t > t:
                break
            cars_before_t = self.all_data.cars_to_run[start_t]
            car_ids = sorted(cars_before_t.keys())
            for car_id in car_ids:
                car = cars_before_t[car_id]
                next_road_id = car.get_next_road_id()
                next_half_road = self.all_data.roads[next_road_id].get_half_road_by_start(car.get_start_cross_id())
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
                car = self.all_data.cars_to_run[start_t][car_id]
                self.all_data.cars_run[car.id] = car
                del self.all_data.cars_to_run[start_t][car_id]
            if not self.all_data.cars_to_run[start_t]:
                del self.all_data.cars_to_run[start_t]

        return dispatch_turns

    def _get_wait_car_direct_by_road_id(self, cross_id, cross, road_id):
        if road_id != -1:
            half_road = self.all_data.roads[road_id].get_half_road_by_direct(cross_id)
            if half_road:
                next_wait_car, _, _ = half_road.get_next_wait_car()
                if next_wait_car:
                    next_road_id = next_wait_car.get_next_road_id()
                    if next_road_id == 'end':
                        return 'D'
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
        half_road.redispatch_step_one_a_lane(next_wait_car_pos[0])

        # 更新下车道状态
        next_half_road.update_next_available_pos()


