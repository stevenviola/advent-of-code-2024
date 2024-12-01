import argparse
import os


class Locations:
    def __init__(self):
        self.location_ids = [[], []]
        self.counts = {}

    def insert_location(self, location_index, num):
        seq = self.location_ids[location_index]
        idx = 0
        if not seq or num > seq[-1]:
            seq.append(num)
        else:
            while num > seq[idx] and idx < len(seq):
                idx += 1
            seq.insert(idx, num)
        if location_index == 1:
            if num not in self.counts:
                self.counts[num] = 0
            self.counts[num] += 1

    def get_total_distances(self):
        ret = 0
        for i in range(len(self.location_ids[0])):
            ret += abs(self.location_ids[0][i] - self.location_ids[1][i])
        return ret

    def get_similarity(self):
        ret = 0
        for i in self.location_ids[0]:
            if i not in self.counts:
                count = 0
            else:
                count = self.counts[i]
            ret += i * count
        return ret


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Historian Hysteria")
    parser.add_argument("filename", help="Path to the input file")
    args = parser.parse_args()
    location = Locations()
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            line = line.strip()
            nums = line.split("   ")
            for num_idx, num in enumerate(nums):
                location.insert_location(num_idx, int(num))
    print(f"Total Disatnces: {location.get_total_distances()}")
    print(f"Total Similarity: {location.get_similarity()}")


if __name__ == "__main__":
    main()
