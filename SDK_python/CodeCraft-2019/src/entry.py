
from dispatcher.dispatch import Dispatcher
from search.search_paths import Searcher
from dispatcher.road import Road
from dispatcher.cross import Cross
from dispatcher.car import Car


def read_param_file(path, cls):
    objects = {}
    with open(path) as f:
        for line in f.readlines():
            line = line.strip()
            if line[0] != '#':
                param = [int(i) for i in line[1:-1].split(',')]
                objects[param[0]] = cls(*[int(i) for i in line[1:-1].split(',')])
    return objects


# def read_roads_file(path):
#     roads = []
#     with open(path) as f:
#         for line in f.readlines():
#             line = line.strip()
#             if line[0] != '#':
#                 param = [int(i) for i in line[1:-1].split(',')]
#                 roads.append(Road(*param[:-1]))
#                 if param[-1]:
#                     roads.append(Road(param[0], param[1], param[2], param[3], param[5], param[4]))
#     return roads


def entry(car_path, road_path, cross_path, answer_path):
    crosses = read_param_file(cross_path, Cross)
    roads = read_param_file(road_path, Road)
    cars = read_param_file(car_path, Car)

    cross_map = list(crosses.keys())
    cross_map.sort()
    crosses_tmp = {}
    for _, c in crosses.items():
        crosses_tmp[cross_map.index(c.id)] = c
        c.id = cross_map.index(c.id)
    crosses = crosses_tmp

    for _, r in roads.items():
        r.start = cross_map.index(r.start)
        r.end = cross_map.index(r.end)
    for _, c in cars.items():
        c.start = cross_map.index(c.start)
        c.end = cross_map.index(c.end)

    total_car_num = len(cars)
    cars_to_run = {}
    cars_run = {}
    cars_complete = {}

    dispatcher = Dispatcher(roads, crosses, cars_to_run, cars_run, cars_complete)
    searcher = Searcher(answer_path, dispatcher, roads, cars, cars_to_run)

    # searcher.open_loop_to_find_paths()

    t = 0
    while cars or cars_to_run or cars_run:
        t += 1

        searcher.search(t)
        dispatcher.dispatch(t)

        # print('time:{} cars:{}/{}'.format(t, len(cars_complete), total_car_num))

    print('调度时间：', t)
    # for _, c in cars_complete.items():
    #     print(c.path)

    with open(answer_path, 'w') as f:
        paths = [c.path_str for _, c in cars_complete.items()]
        f.writelines('\n'.join(paths))

