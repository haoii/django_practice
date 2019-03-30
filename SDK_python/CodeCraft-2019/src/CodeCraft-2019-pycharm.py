import logging

from entry import entry

ROOT_PATH = '../'

logging.basicConfig(level=logging.DEBUG,
                    filename=ROOT_PATH + '../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():

    car_path = ROOT_PATH + 'config/car.txt'
    road_path = ROOT_PATH + 'config/road.txt'
    cross_path = ROOT_PATH + 'config/cross.txt'
    answer_path = ROOT_PATH + 'config/answer.txt'

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    entry(car_path, road_path, cross_path, answer_path)


if __name__ == "__main__":
    main()
