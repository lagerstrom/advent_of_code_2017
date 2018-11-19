#!/usr/bin/env python3

import math

class Virus:
    def __init__(self):
        self.direction = 'up'
        self.x = 0
        self.y = 0
        self.direction_dict = {
            'up': (0, -1),
            'right': (1, 0),
            'down': (0, 1),
            'left': (-1, 0)
        }

    def get_next(self, input_list):
        for i, d in enumerate(input_list):
            if d == self.direction:
                return input_list[(i + 1) % len(input_list)]

    def update_direction(self, infected):
        if infected:
            directions = ['up', 'right', 'down', 'left']
            self.direction = self.get_next(directions)
        else:
            directions = ['up', 'left', 'down', 'right']
            self.direction = self.get_next(directions)

    def move(self):
        #print('I will move {}'.format(self.direction))
        self.x += self.direction_dict[self.direction][0]
        self.y += self.direction_dict[self.direction][1]

    def get_current_position(self):
        return self.x, self.y

class Nodes:
    def __init__(self):
        self.infected_nodes = []
        self.parse_input('big_input.txt')

    def parse_input(self, filename):
        all_lines = [[]]
        line_num = 0
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if line == '':
                    break
                line_num += 1

                all_lines.append(list(line.strip()))
        all_lines.remove([])

        middle = math.floor(line_num / 2)

        for y in range(0, line_num):
            for x in range(0, line_num):
                if all_lines[y][x] == '#':
                    v_x = x - middle
                    v_y = y - middle
                    self.add_infection((v_x, v_y))

    def add_infection(self, coordinates):
        self.infected_nodes.append(coordinates)

    def remove_infection(self, coordinates):
        self.infected_nodes.remove(coordinates)

    def is_infected(self, coordinates):
        for node in self.infected_nodes:
            if node == coordinates:
                return True
        return False

    def pretty_print(self, size, virus_coordinates=None):
        middle = math.floor(size / 2)

        for y in range(((middle * -1)), middle + 1):
            current_line = ''
            for x in range(((middle * -1)), middle + 1):
                if (x, y) == virus_coordinates:
                    curret_list = list(current_line)
                    curret_list[-1] = '['
                    current_line = ''.join(curret_list)
                if self.is_infected((x, y)):
                    current_line += '#'
                else:
                    current_line += '.'
                if (x, y) == virus_coordinates:
                    current_line += ']'
                else:
                    current_line += ' '
            print(current_line)



def main():
    infections = 0
    v = Virus()

    node_map = Nodes()

    for x in range(0, 10000):
        if node_map.is_infected(v.get_current_position()):
            v.update_direction(True)
            node_map.remove_infection(v.get_current_position())
        else:
            v.update_direction(False)
            node_map.add_infection(v.get_current_position())
            infections += 1

        v.move()
    print(infections)


if __name__ == '__main__':
    main()
