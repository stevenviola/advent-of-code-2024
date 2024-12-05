import argparse
import os


class Wordsearch:
    def __init__(self):
        self.board = []
        self.height = 0
        self.width = 0
        self.xmas_count = 0
        self.x_mas_count = 0

    def add_line(self, line):
        self.board.append(line)
        self.height += 1
        self.width = len(line)

    def search_direction(self, y, x, direction, word):
        """Helper function to search in a specific direction."""
        for i in range(len(word)):
            nx, ny = x + direction[0] * i, y + direction[1] * i
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                return False
            if self.board[ny][nx] != word[i]:
                return False
        return True

    def search(self, word):
        for direction in (
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (-1, -1),
            (-1, 1),
            (1, 1),
            (1, -1),
        ):
            for y in range(self.height):
                for x in range(self.width):
                    if self.search_direction(y, x, direction, word):
                        self.xmas_count += 1

    def x_search(self, word):
        middle_letter = word[int(len(word) / 2)]
        words = (word, word[::-1])
        for y, row in enumerate(self.board):
            for x, letter in enumerate(row):
                if letter == middle_letter:
                    if not (
                        1 <= x < self.width - 1 and 1 <= y < self.height - 1
                    ):
                        continue
                    left = (
                        self.board[y - 1][x - 1]
                        + letter
                        + self.board[y + 1][x + 1]
                    )
                    right = (
                        self.board[y + 1][x - 1]
                        + letter
                        + self.board[y - 1][x + 1]
                    )
                    if left in words and right in words:
                        self.x_mas_count += 1


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Ceres Search")
    parser.add_argument("filename", help="Path to the input file")
    args = parser.parse_args()
    wordsearch = Wordsearch()
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            line = list(line.strip())
            wordsearch.add_line(line)
    wordsearch.search("XMAS")
    wordsearch.x_search("MAS")
    print(f"XMAS found {wordsearch.xmas_count} times")
    print(f"X-MAS found {wordsearch.x_mas_count} times")


if __name__ == "__main__":
    main()
