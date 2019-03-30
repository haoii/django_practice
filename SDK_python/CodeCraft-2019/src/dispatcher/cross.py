
class Cross:
    direct_table = {1: 'L', 2: 'D', 3: 'R'}
    delta_table = {'L': 1, 'D': 2, 'R': 3}

    def __init__(self, all_data, id, road_id1, road_id2, road_id3, road_id4):
        self.id = id
        self.road_id1 = road_id1
        self.road_id2 = road_id2
        self.road_id3 = road_id3
        self.road_id4 = road_id4

        self.road_ids = [self.road_id1, self.road_id2, self.road_id3, self.road_id4]

        self.is_border = self.road_num() == 3
        self.dist_to_border = 0 if self.is_border else 10000000

    def road_num(self):
        return 4 - self.road_ids.count(-1)

    def id_ordered_road_ids(self):
        return sorted(self.road_ids)

    def get_direct(self, from_id, to_id):
        from_no, to_no = self.road_ids.index(from_id), self.road_ids.index(to_id)
        delta = to_no - from_no
        delta = delta if delta > 0 else delta + 4
        return self.direct_table[delta]

    def get_road_id_by_direct(self, from_id, direct):
        from_no = self.road_ids.index(from_id)
        to_no = from_no + self.delta_table[direct]
        to_no = to_no if to_no < 4 else to_no - 4
        return self.road_ids[to_no]

    def __str__(self):
        return '路口' + str(self.id) + \
               '-道路' + str(self.road_id1) + \
               '-道路' + str(self.road_id2) + \
               '-道路' + str(self.road_id3) + \
               '-道路' + str(self.road_id4)

