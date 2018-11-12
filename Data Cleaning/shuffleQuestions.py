from random import shuffle

with open("../data/input/QALD-questions-stripped.txt", "r") as file:
    lines = file.readlines()
    shuffle(lines)
    with open("../data/input/QALD-shuffled.txt", "w") as outfile:
        for line in lines:
            outfile.write(line)
