import argparse
import os


class Reactor:
    def __init__(self):
        self.safe = 0
        self.loosly_safe = 0

    def retry_process(self, line):
        for i in range(len(line)):
            if self.process_report(line, i):
                return True
        return False

    def process_report(self, report, remove=None):
        line = report.copy()
        if remove is not None:
            del line[remove]
        prev = None
        incrementing = line[1] - line[0] > 0
        for i in line:
            if prev is not None:
                diff = prev - i
                abs_diff = abs(diff)
                if (
                    abs_diff < 1
                    or abs_diff > 3
                    or (abs_diff == diff) is incrementing
                ):
                    return (
                        self.retry_process(line) if remove is None else False
                    )
            prev = i
        self.loosly_safe += 1
        if remove is None:
            self.safe += 1
        return True


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Red-Nosed Reports")
    parser.add_argument("filename", help="Path to the input file")
    args = parser.parse_args()
    reactor = Reactor()
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            line = line.strip()
            line = [int(x) for x in line.split(" ")]
            reactor.process_report(line)
    print(f"Sum of Safe Reports: {reactor.safe}")
    print(f"Sum of Loosly Safe Reports: {reactor.loosly_safe}")


if __name__ == "__main__":
    main()
