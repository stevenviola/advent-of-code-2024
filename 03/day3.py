import argparse
import os
import re


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Mull It Over")
    parser.add_argument("filename", help="Path to the input file")
    args = parser.parse_args()
    sums = {True: 0, False: 0}
    do = True
    with open(f"{path}/{args.filename}", "r") as f:
        data = f.read()
        i = 0
        while i < len(data):
            find = "don't()" if do else "do()"
            next = data[i:].find(find)
            if next < 0:
                next = len(data) - i + 1
            substring = data[i : i + next]
            match = re.findall(r"mul\((\d+),(\d+)\)", substring, re.DOTALL)
            for j in match:
                sums[do] += int(j[0]) * int(j[1])
            i += next
            do = not do

    print(f"Sum of multiplications is: {sum(sums.values())}")
    print(f"Sum of Enabled multiplications is: {sums[True]}")


if __name__ == "__main__":
    main()
