import subprocess
import pathlib
import collections
from EasyCCGTrees.to_tree import to_tree, print_tree
# from EasyCCGTrees.Visualize import build

EASYCCG_HOME = pathlib.Path("/opt/easyccg/")
OUT_PATH = pathlib.Path("/tmp/")

def run_easyCCG(input_path):
    with open(OUT_PATH/"ccgout.txt", "w") as outfile:
        subprocess.run(["java", "-jar", str(EASYCCG_HOME/"easyccg.jar"), "-f", input_path,
            "--model", str(EASYCCG_HOME/"model_questions")],
                stdout = outfile)

def remove_IDs():
    with open(OUT_PATH/"ccgout.txt") as origfile:
        with open(OUT_PATH/"ccgout_stripped.txt", "w") as newfile:
            for count, line in enumerate(origfile):
                if count % 2 == 1:
                    print(line.rstrip(), file = newfile)

def tree_equals(tree1, tree2):
    if not tree1.children and not tree2.children:
        return True
    elif len(tree1.children) != len(tree2.children):
        return False
    else:
        return tree1.name == tree2.name and \
            all(tree_equals(child1, child2) for (child1, child2) in zip(tree1.children, tree2.children))

def label(text):
    with open(OUT_PATH/"_labeltmp","w") as tmpfile:
        tmpfile.write(text)
    proc = subprocess.run(["java", "-jar", str(EASYCCG_HOME/"easyccg.jar"), "-f", "/tmp/_labeltmp",
        "--model", str(EASYCCG_HOME/"model_questions")], capture_output = True)

    return str(proc.stdout.rstrip())

def group(file):
    with open(file) as input_file:
        pass

if __name__ == "__main__":
    run_easyCCG("QALD-questions.txt-stripped.txt")
    remove_IDs()
    tree = None
    with open(OUT_PATH/"ccgout_stripped.txt") as f:
        first = f.readline().rstrip()
        tree = to_tree(first)
        # print_tree(to_tree(first))

    second = to_tree(r"(<T S[wq] 0 2> (<T S[wq]/(S[dcl]\NP) 0 2> (<L (S[wq]/(S[dcl]\NP))/N POS POS Which (S[wq]/(S[dcl]\NP))/N>) (<L N POS POS presidents N>) ) (<T S[dcl]\NP 0 2> (<L (S[dcl]\NP)/(S[pss]\NP) POS POS were (S[dcl]\NP)/(S[pss]\NP)>) (<T S[pss]\NP 0 2> (<L S[pss]\NP POS POS born S[pss]\NP>) (<T (S\NP)\(S\NP) 0 2> (<L ((S\NP)\(S\NP))/NP POS POS in ((S\NP)\(S\NP))/NP>) (<T NP 0 1> (<L N POS POS 1945? N>) ) ) ) ) )")
    # print(type(first))
    # print(type(second))

    # print(label("Which presidents were born in 1945?"))
    test1 = to_tree(label("What presidents were born in 1945"))
    test2 = to_tree(label("Which presidents were born in 1945"))
    test3 = to_tree(label("Which presidents were not born in 1945"))

    print(tree_equals(test1,test2))
    print(tree_equals(test1,test3))
