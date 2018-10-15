with open("QALD-questions.txt", "r") as infile:
    with open("QALD-questions-unnumbered-.txt", "w") as outfile:
        for line in infile.readlines():
            write = line.split()[1:]
            outfile.write(" ".join(write) + "\n")
