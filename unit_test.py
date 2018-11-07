from groupLines import *
from to_tree import *

test_cases = ["What presidents were born in 1945?",
              "Which presidents were born in 1946",
              "Which presidents were not born in 1945",
              "How tall is John Windsor",
              "How tall is Kate Upton"]

if __name__ == '__main__':
    labels = label("\n".join(test_cases))
    trees = [CCGNode.from_ccg(l) for l in labels]
    output_tree(trees[2] & trees[1] & trees[0])
