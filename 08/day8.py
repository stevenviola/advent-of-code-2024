import argparse
import os


class Frequency:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.locations = set()
        self.antinodes = set()
        self.resonances = set()

    def add_antenna(self, pos):
        self.get_antinodes(pos)
        self.locations.add(pos)

    def get_antinodes(self, pos):
        for i in self.locations:
            diff_x = i[0] - pos[0]
            diff_y = i[1] - pos[1]
            for j, x in ((i, 1), (pos, -1)):
                for multiplier in range(1, max(self.width, self.height) + 2):
                    new_x = j[0] + (x * multiplier * diff_x)
                    new_y = j[1] + (x * multiplier * diff_y)
                    if not (
                        0 <= new_x < self.width and 0 <= new_y < self.height
                    ):
                        break
                    if multiplier == 1:
                        self.antinodes.add((new_x, new_y))
                    else:
                        self.resonances.add((new_x, new_y))


def main() -> None:
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Resonant Collinearity")
    parser.add_argument("filename", help="Path to the input file")
    args = parser.parse_args()
    frequencies = {}
    with open(f"{path}/{args.filename}", "r") as f:
        height = len(f.readlines())
        f.seek(0)
        for y, line in enumerate(f):
            line = line.strip()
            width = len(line)
            for x, letter in enumerate(line):
                if letter == ".":
                    continue
                if letter not in frequencies:
                    frequencies[letter] = Frequency(width, height)
                frequencies[letter].add_antenna((x, y))

    total_antinodes = set()
    total_antinodes_with_resonances = set()
    for x in frequencies:
        total_antinodes = total_antinodes | frequencies[x].antinodes
        total_antinodes_with_resonances = (
            total_antinodes_with_resonances | frequencies[x].locations
        )
        total_antinodes_with_resonances = (
            total_antinodes_with_resonances | frequencies[x].resonances
        )
    total_antinodes_with_resonances = (
        total_antinodes_with_resonances | total_antinodes
    )
    print(
        f"There are a total of {len(total_antinodes)} "
        + "antinodes for all frequencies"
    )
    print(
        f"There are a total of {len(total_antinodes_with_resonances)} "
        + "antinodes with resonances for all frequencies"
    )


if __name__ == "__main__":
    main()
