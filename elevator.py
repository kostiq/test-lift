import argparse
import threading
from time import sleep

MIN_FLOW_NUMBER=5
MAX_FLOW_NUMBER = 20


class Elevator(object):
    _current_position = 0
    _closing_time = 0
    _work = False
    _time_between_floors = 0
    _command_list = []
    _changed = False

    def __init__(self, time, closing_time, *args, **kwargs):
        self._time_between_floors = time
        self._closing_time = closing_time

    def elevator_on_floor(self, floor):
        print('Opening doors')
        sleep(self._closing_time)
        print('Closing doors')
        sleep(self._closing_time)
        self.done_commands(floor)

    def get_current_position(self):
        return self._current_position

    def add_command(self, floor):
        self._changed = True
        self._command_list.append(floor)
        command_list = self.get_command_list()
        if self._changed:
            command_list = sorted(command_list, key=lambda x: abs(x - self.get_current_position()))
            self._changed = False

    def get_command_list(self):
        return self._command_list

    def travel_to_floor(self, floor, direction_up):
        current_position = self.get_current_position()
        if direction_up:
            floors_list = range(current_position, floor + 1)
        else:
            floors_list = reversed(range(floor, current_position + 1))

        for floor_number in floors_list:
            sleep(self._time_between_floors)
            print('Elevator on {} floor'.format(floor_number))
            self._current_position = floor_number
        self.elevator_on_floor(floor)

    def done_commands(self, floor):
        while floor in self.get_command_list():
            self.get_command_list().remove(floor)

    def do(self):
        while True:
            for floor in self.get_command_list():
                if floor > self.get_current_position():
                    self.travel_to_floor(floor, True)
                elif floor < self.get_current_position():
                    self.travel_to_floor(floor, False)
                else:
                    self.elevator_on_floor(floor)


def input_command():
    while True:
        floor = input('Input flow number:')
        try:
            floor = int(floor)
            if MIN_FLOW_NUMBER <= floor <= MAX_FLOW_NUMBER:
                yield floor
            else:
                print('Input number from 5 to 20!')
        except Exception as e:
            print('Input correct number!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--floors', type=int, required=True)
    parser.add_argument('-fh', '--floorheight', type=int, required=True)
    parser.add_argument('-s', '--speed', type=int, required=True)
    parser.add_argument('-d', '--delayonfloor', type=int, required=True)
    args = parser.parse_args()

    elevator = Elevator(args.floorheight / args.speed, args.delayonfloor)

    t = threading.Thread(target=elevator.do)
    t.deamon = True
    t.start()

    for floor in input_command():
        elevator.add_command(floor)
