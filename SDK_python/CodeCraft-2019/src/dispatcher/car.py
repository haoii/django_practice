
from enum import Enum

CarStatus = Enum('CarStatus', 'home init wait stop complete')


class Car:
    def __init__(self, all_data, id, start, end, max_v, planned_time):
        self.id = id
        self.start = start
        self.end = end
        self.max_v = max_v
        self.planned_time = planned_time

        self.path = None
        self.start_t = None
        self.status = CarStatus.home
        self.cur_pos = -1
        self.last_r = None

    def get_path_str(self):
        return '(' + str(self.id) + ',' + str(self.start_t) + ',' + ','.join([str(p.id) for p in self.path[:-1]]) + ')'

    def is_last_path(self):
        return self.path[self.cur_pos + 1] == 'end'

    def go_next_road(self):
        self.cur_pos += 1

    def get_next_road_id(self):
        if self.is_last_path():
            return 'end'
        return self.path[self.cur_pos + 1].id

    def get_start_cross_id(self):
        return self.start

    # def is_last_path(self):
    #     return self.path[self.path[self.cur_pos]] == 'end'
    #
    # def go_next_road(self):
    #     self.cur_pos = self.path[self.path[self.cur_pos]]
    #
    # def get_next_road_id(self):
    #     next_path = self.path[self.path[self.cur_pos]]
    #     return int(next_path[1:])
    #
    # def get_start_cross_id(self):
    #     return int(self.path['start'][1:])

    def __str__(self):
        return '车辆' + str(self.id) + \
               '-起点' + str(self.start) + \
               '-终点' + str(self.end) + \
               '-限速' + str(self.max_v) + \
               '-计划出发时间' + str(self.planned_time) + \
               '-状态' + str(self.status)

