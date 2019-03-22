import logging
import sys

from dispatch import Dispatcher

ROOT_PATH = ''  # ''../'

logging.basicConfig(level=logging.DEBUG,
                    filename=ROOT_PATH + '../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    # car_path = ROOT_PATH + 'config/car.txt'
    # road_path = ROOT_PATH + 'config/road.txt'
    # cross_path = ROOT_PATH + 'config/cross.txt'
    # answer_path = ROOT_PATH + 'config/answer.txt'

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    dispatcher = Dispatcher(car_path, road_path, cross_path, answer_path)


if __name__ == "__main__":
    main()