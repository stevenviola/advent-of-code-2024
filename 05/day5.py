import argparse
import os


class Printer:
    def __init__(self):
        self.before = {}
        self.after = {}
        self.sum_middles_correct = 0
        self.sum_middles_incorrect = 0

    def add_order(self, order):
        if order[1] not in self.before:
            self.before[order[1]] = set()
        if order[0] not in self.after:
            self.after[order[0]] = set()
        self.before[order[1]].add(order[0])

    def sort_pages(self, pages):
        sorted_order = []
        for num in pages:
            self.get_no_dependents(pages, sorted_order, num)
        middle = int(len(sorted_order) / 2)
        if pages == sorted_order:
            print("This line already sorted")
            self.sum_middles_correct += sorted_order[middle]
        else:
            print(f"Sorted this line: {sorted_order}")
            self.sum_middles_incorrect += sorted_order[middle]
        return list(sorted_order)

    def get_no_dependents(self, pages, sorted_order, num):
        if num in self.before:
            for befores in self.before[num]:
                if befores in pages:
                    self.get_no_dependents(pages, sorted_order, befores)
                    if befores not in sorted_order:
                        sorted_order.append(befores)
        if num not in sorted_order:
            sorted_order.append(num)


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Print Queue")
    parser.add_argument("filename", help="Path to the input file")
    args = parser.parse_args()
    printer = Printer()
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            line = line.strip()
            if "|" in line:
                printer.add_order([int(x) for x in line.split("|")])
            elif "," in line:
                print(f"Sorting {line}")
                printer.sort_pages([int(x) for x in line.split(",")])

    print(f"Sum of correct middles is {printer.sum_middles_correct}")
    print(f"Sum of sorted middles is {printer.sum_middles_incorrect}")


if __name__ == "__main__":
    main()
