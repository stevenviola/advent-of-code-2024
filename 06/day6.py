import argparse
import copy
import os


class GuardPatrol:
    def __init__(
        self,
        map=[],
        guard_pos=None,
        guard_dir=[0, -1],
        guard_origin=None,
        obs_test=False,
    ):
        self.map = map
        self.guard_pos = guard_pos
        self.guard_dir = guard_dir
        self.guard_origin = guard_origin
        self.obstruction_test = obs_test
        self.guard_positions = set()
        self.guard_historical_directions = {}
        self.obstructions = set()

    def add_row(self, row):
        new_row = []
        for i in row:
            if i == "#":
                new_row.append(i)
            elif i == ".":
                new_row.append([])
            elif i == "^":
                y = len(self.map)
                x = row.index("^")
                self.guard_pos = (x, y)
                self.guard_origin = (x, y)
                self.guard_positions.add(self.guard_pos)
                new_row.append([[0, -1]])
        self.map.append(new_row)

    def rotate_cw(self):
        if self.guard_dir == [0, -1]:
            return [1, 0]
        elif self.guard_dir == [1, 0]:
            return [0, 1]
        elif self.guard_dir == [0, 1]:
            return [-1, 0]
        elif self.guard_dir == [-1, 0]:
            return [0, -1]

    def is_inbounds(self, pos=None):
        if pos is None:
            pos = self.guard_pos
        if not (
            0 <= pos[1] < len(self.map) and 0 <= pos[0] < len(self.map[0])
        ):
            return False
        return True

    def get_next_pos(self):
        new_x = self.guard_pos[0] + self.guard_dir[0]
        new_y = self.guard_pos[1] + self.guard_dir[1]
        new_pos = (new_x, new_y)
        if not self.is_inbounds(new_pos):
            return (None, None)
        if self.map[new_y][new_x] == "#":
            return (self.guard_pos, self.rotate_cw())
        return (new_pos, (self.guard_dir))

    def guard_walk(self):
        while self.is_inbounds():
            new_pos, new_dir = self.get_next_pos()
            if new_pos is None:
                return
            if new_pos is not self.guard_pos:
                if not self.obstruction_test:
                    if new_pos not in self.guard_positions:
                        new_map = copy.deepcopy(self.map)
                        new_map[new_pos[1]][new_pos[0]] = "#"
                        self.test_obstruction(new_map, new_pos)
                if self.guard_dir in self.map[new_pos[1]][new_pos[0]]:
                    return False
            self.guard_positions.add(new_pos)
            self.guard_pos = new_pos
            self.guard_dir = new_dir
            self.map[new_pos[1]][new_pos[0]].append(new_dir)

    def test_obstruction(self, new_map, new_pos):
        if new_pos == self.guard_origin:
            return
        gp = GuardPatrol(
            new_map, self.guard_pos, self.guard_dir, self.guard_origin, True
        )
        if gp.guard_walk() is False:
            self.obstructions.add(new_pos)


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Guard Gallivant")
    parser.add_argument("filename", help="Path to the input file")
    args = parser.parse_args()
    gp = GuardPatrol()
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            line = line.strip()
            gp.add_row(list(line))
    gp.guard_walk()
    print(f"The guard visited {len(gp.guard_positions)} distinct positions")
    print(f"There are {len(gp.obstructions)} possible obstruction points")


if __name__ == "__main__":
    main()
