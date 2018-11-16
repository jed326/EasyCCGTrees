from random import shuffle
from collections import OrderedDict


def removeNumbers():
    with open("./input/QALD-questions.txt", "r") as infile:
        with open("./input/QALD-questions-stripped.txt", "w") as outfile:
            for line in infile.readlines():
                write = line.split()[1:]
                outfile.write(" ".join(write) + "\n")

def shuffle():
    with open("./input/QALD-questions-stripped.txt", "r") as file:
        lines = file.readlines()
        shuffle(lines)
        with open("./input/QALD-shuffled.txt", "w") as outfile:
            for line in lines:
                outfile.write(line)

def removeDuplicates():
    with open("./input/QALD-questions-stripped.txt", "r") as file:
        lines = file.readlines()
        noDups = list(OrderedDict.fromkeys(lines))
        with open("./input/QALD-no-duplicates.txt", "w") as outfile:
            for line in noDups:
                outfile.write(line)

if __name__ == "__main__":
    removeDuplicates()
