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

    def update_direction(self, node_status):
        if node_status == 'infected':
            directions = {
                'up': 'right',
                'right': 'down',
                'down': 'left',
                'left': 'up'
            }
            self.direction = directions[self.direction]
        if node_status == 'clean':
            directions = {
                'up': 'left',
                'left': 'down',
                'down': 'right',
                'right': 'up'
            }
            self.direction = directions[self.direction]
        if node_status == 'flagged':
            reverse_directions = {
                'up': 'down',
                'down': 'up',
                'left': 'right',
                'right': 'left'
            }
            self.direction = reverse_directions[self.direction]

    def move(self):
        self.x += self.direction_dict[self.direction][0]
        self.y += self.direction_dict[self.direction][1]

    def get_current_position(self):
        return self.x, self.y


class Nodes:
    def __init__(self):
        self.node_dict = {}
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
                    self.node_dict[(v_x, v_y)] = 'infected'

    def switch_state(self, coordinates):
        states = {
            'clean': 'weakend',
            'weakend': 'infected',
            'infected': 'flagged',
            'flagged': 'clean'
        }

        self.node_dict[coordinates] = states[self.get_node_status(coordinates)]

    def get_node_status(self, coordinates):
        if coordinates in self.node_dict:
            return self.node_dict[coordinates]
        else:
            return 'clean'

    def pretty_print(self, size, virus_coordinates=None):
        middle = math.floor(size / 2)

        state_dict = {
            'clean': '.',
            'weakend': 'W',
            'infected': '#',
            'flagged': 'F'
        }

        for y in range(((middle * -1)), middle + 1):
            current_line = ''
            for x in range(((middle * -1)), middle + 1):
                if (x, y) == virus_coordinates:
                    curret_list = list(current_line)
                    curret_list[-1] = '['
                    current_line = ''.join(curret_list)

                current_line += state_dict[self.get_node_status((x, y))]

                if (x, y) == virus_coordinates:
                    current_line += ']'
                else:
                    current_line += ' '
            print(current_line)


def main():
    infections = 0
    v = Virus()

    node_map = Nodes()


    for x in range(0, 10000000):
        virust_coordinates = v.get_current_position()
        node_status = node_map.get_node_status(virust_coordinates)
        v.update_direction(node_status)
        node_map.switch_state(virust_coordinates)
        v.move()

        if node_status == 'weakend':
            infections += 1

    print(infections)


if __name__ == '__main__':
    main()
