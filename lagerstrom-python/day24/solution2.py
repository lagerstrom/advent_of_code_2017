#!/usr/bin/env python3

all_components2 = {
    0: [(0, 2), (0, 1)],
    1: [(0, 1), (10, 1)],
    2: [(0, 2), (2, 2), (2, 3)],
    3: [(2, 3), (3, 4), (3, 5)],
    4: [(3, 4)],
    5: [(3, 5)],
    6: [],
    7: [],
    8: [],
    9: [(9, 10)],
    10: [(10, 1), (9, 10)]
}




class Bridge:
    def __init__(self):
        self.__bridge_components = set()
        self.__last_component = ()
        self.__next_num = 0

    def add_component(self, component, current_num):
        self.__bridge_components.add(component)
        self.__last_component = component

        if current_num == component[0]:
            self.__next_num = component[1]
        else:
            self.__next_num = component[0]

    def component_in_bridge(self, component):
        return component in self.__bridge_components

    def get_last_component(self):
        return self.__last_component

    def get_bridge(self):
        return self.__bridge_components

    def get_next_port(self):
        return self.__next_num

    def calculate_score(self):
        score = 0
        for component in self.get_bridge():
            score += (component[0] + component[1])
        return score

    def __len__(self):
        return len(self.__bridge_components)


def parse_input(input_file):
    ret_dict = {}

    with open(input_file, 'r') as f:
        while True:
            line = f.readline().strip()
            if line == '':
                break

            sp_line = list(map(int, line.split('/')))
            tmp_set = (sp_line[0], sp_line[1])

            if sp_line[0] not in ret_dict:
                ret_dict[sp_line[0]] = set()
            if sp_line[1] not in ret_dict:
                ret_dict[sp_line[1]] = set()

            ret_dict[sp_line[0]].add(tmp_set)
            ret_dict[sp_line[1]].add(tmp_set)
    return ret_dict

def main():

    all_components = parse_input('big_input.txt')


    all_bridges = []

    for component in all_components[0]:
        bridge = Bridge()
        bridge.add_component(component, 0)
        all_bridges.append(bridge)


    for bridge in all_bridges:
        for component in all_components[bridge.get_next_port()]:
            if not bridge.component_in_bridge(component):
                new_bridge = Bridge()
                for old_component in bridge.get_bridge():
                    new_bridge.add_component(old_component, bridge.get_next_port())
                new_bridge.add_component(component, bridge.get_next_port())
                all_bridges.append(new_bridge)


    longest_bridge = Bridge()

    for bridge in all_bridges:
        if len(bridge) >= len(longest_bridge):
            if len(bridge) == len(longest_bridge):
                if bridge.calculate_score() > longest_bridge.calculate_score():
                    longest_bridge = bridge
            else:
                longest_bridge = bridge

    print(longest_bridge.get_bridge())
    print(longest_bridge.calculate_score())
if __name__ == '__main__':
    main()