from groupLines import *

if __name__ == '__main__':
    run_easyCCG("QALD-questions.txt-stripped.txt")
    remove_IDs()
    tree = None
    with open(OUT_PATH / "ccgout_stripped.txt") as f:
        first = f.readline().rstrip()
        tree = to_tree(first)
        # print_tree(to_tree(first))
    second = to_tree(
        r"(<T S[wq] 0 2> (<T S[wq]/(S[dcl]\NP) 0 2> (<L (S[wq]/(S[dcl]\NP))/N POS POS Which (S[wq]/(S[dcl]\NP))/N>) (<L N POS POS presidents N>) ) (<T S[dcl]\NP 0 2> (<L (S[dcl]\NP)/(S[pss]\NP) POS POS were (S[dcl]\NP)/(S[pss]\NP)>) (<T S[pss]\NP 0 2> (<L S[pss]\NP POS POS born S[pss]\NP>) (<T (S\NP)\(S\NP) 0 2> (<L ((S\NP)\(S\NP))/NP POS POS in ((S\NP)\(S\NP))/NP>) (<T NP 0 1> (<L N POS POS 1945? N>) ) ) ) ) )")
    # print(type(first))
    # print(type(second))

    # print(label("Which presidents were born in 1945?"))
    test1 = to_tree(label("What presidents were born in 1945?"))
    # test2 = to_tree(label("Which presidents were born in 1946"))
    # test3 = to_tree(label("Which presidents were not born in 1945"))
    #
    test4 = to_tree(label("How tall is John Windsor"))
    # test5 = to_tree(label("How tall is Kate Upton"))

    # print(label("How tall is John Windsor"))
    # print_tree(test4)

    print_tree(test1)
    print_tree(test4)

    print(tree_equals(test1, test4, 0, 0))
