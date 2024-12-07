import argparse
import os


class Calibrations:
    def __init__(self, target, operators) -> None:
        self.operators = operators
        self.target = target
        self.target_found = False

    def do_math(self, numbers, operation) -> int:
        if operation == "+":
            return numbers[0] + numbers[1]
        elif operation == "*":
            return numbers[0] * numbers[1]
        elif operation == "||":
            return int(str(numbers[0]) + str(numbers[1]))

    def all_options(self, numbers, last) -> int:
        if len(numbers) < 1:
            return last
        for j in self.operators:
            if self.target_found:
                return
            total = self.all_options(
                numbers[1:], self.do_math((last, numbers[0]), j)
            )
            if total == self.target:
                self.target_found = True

    def process_line(self, line) -> int:
        numbers = [int(x) for x in line.split(":")[1].strip().split()]
        self.all_options(numbers[1:], numbers[0])
        if self.target_found:
            return self.target
        return 0


def main() -> None:
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Bridge Repair")
    parser.add_argument("filename", help="Path to the input file")
    args = parser.parse_args()
    sum_of_valid = {2: 0, 3: 0}
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            line = line.strip()
            target = int(line.split(":")[0])
            ops = ("+", "*", "||")
            for i in range(2, 4):
                c = Calibrations(target, ops[:i])
                sum_of_valid[i] += c.process_line(line)
    for i in range(2, 4):
        print(f"The sum of valid calibrations is {sum_of_valid[i]}")


if __name__ == "__main__":
    main()
