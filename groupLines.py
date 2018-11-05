import subprocess
import pathlib
import collections
import argparse
from to_tree import to_tree, print_tree
# from EasyCCGTrees.Visualize import build
import itertools
import os

# REQUIRED: Input path argument
# OPTIONAL: ouput path argument

'''
Environment Setup
'''
EASYCCG_HOME = pathlib.Path(os.environ.get("EASYCCG_HOME", "./easyccg"))
if "EASYCCG_HOME" not in os.environ:
    print("Didn't find EASYCCG_HOME variable, looking for local copy in current directory.")
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

def firstWord(tree):

    if tree.children:
        return firstWord(tree.children[0])

    else:
        return tree.name

def naive_equals(tree1, tree2):
    return firstWord(tree1) == firstWord(tree2)

def tree_equals(tree1, tree2, tolerance = 0, limit = 2):
    if tolerance > limit:
        return True
    if not tree1.children and not tree2.children:
        return True
    elif len(tree1.children) != len(tree2.children):
        return False
    else:
        return tree1.name == tree2.name and \
            all(tree_equals(child1, child2, tolerance + 1, limit) for (child1, child2) in zip(tree1.children, tree2.children))

def label(text):
    with open(OUT_PATH/"_labeltmp","w") as tmpfile:
        tmpfile.write(text)
    proc = subprocess.run(["java", "-jar", str(EASYCCG_HOME/"easyccg.jar"), "-f", "/tmp/_labeltmp",
        "--model", str(EASYCCG_HOME/"model_questions")], capture_output = True)

    return proc.stdout.decode("utf-8").split("\n")[1::2]

'''
    eq_fn - function taking two trees (and optional kwargs) as input,
    returning True if they are equal and False otherwise. eq_fn should
    be transitive, i.e. if a = b and b = c, then a = c

    file_path - relative (or absolute) path to file containing newline
    separated questions to parse
'''

def group(file_path, out_path = "./_grouped_out.txt", eq_fn = tree_equals, **kwargs):
    #categories is a list of dictionaries
    #each index is a mapping between the parsed question and its tree representation
    #labelled is a dictionary that maps the parsed question to the original question
    categories = []
    labelled = {}

    with open(file_path) as input_file:
        #labelled = {label(line)[0]: line for line in input_file}
        labelled_list = label(input_file.read())
        #labelled = label(input_file.read())
        input_file.seek(0)
        # original_questions = [label,orig for label,orig in zip(labelled_list, input_file)]
        # labelled = {}
        # for orig in original_questions:
        #     labelled.update
        labelled = {label : str(i) + " " + orig for i,(label,orig) in enumerate(zip(labelled_list, input_file))}

    #labelled = labelled[:20]
    #print(labelled)

    trees = {label: to_tree(label) for label in labelled.keys()}
    #trees = list(map(labelled, to_tree))
    #print("\n".join(labelled[:10]))

    for line, tree in trees.items():
        for category in categories:

            #get an arbitrary tree from category
            firstTree = next(iter(category.values()))

            #this category matches, so move on to the next tree
            if eq_fn(tree, firstTree):
                category[line] = tree
                break
        else:
            categories.append({line: tree})

    # TODO: Make this into a function call
    categories.sort(key=len, reverse=True)
    with open(out_path, "w") as grouped_file:
        grouped_file.write("%d categories were found\n\n" % (len(categories)))
        n = 1
        for category in categories:
            questions = [str(labelled[parse]) for parse in category.keys()]
            # print(sentences)
            wh_words = {}
            for question in questions:
                word = question.split()[1]
                if word in wh_words.keys():
                    wh_words[word] += 1
                else:
                    wh_words.update({word:1})
            # print(wh_words)

            wh_words_percentages = []
            for word in wh_words.keys():
                wh_words_percentages.append("%s (%.2f%%)" % (word, wh_words[word]/len(category)*100))

            print(wh_words_percentages)


            grouped_file.write("Category %d: contains %d questions with wh-words [%s]\n" % (n, len(category), ", ".join(wh_words_percentages)))
            grouped_file.write("".join(str(labelled[parse]) for parse in category.keys()))
            grouped_file.write("\n")
            n += 1

    print("Created %d categories, written to %s" % (len(categories), out_path))

def _test():
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

    print(tree_equals(test1,test4, 0, 0))
    # print(tree_equals(test1,test3))
    # print(tree_equals(test4,test5))


if __name__ == "__main__":
    #TODO: add flags for printing tagged form or normal form; possibly have common tree at the top of each category
    #or print out list of categories,where each category is just one tree
    #or output
    #parameter for depth
    #take in list of categories
    parser = argparse.ArgumentParser(description="Group similar questions into categories")
    parser.add_argument("path", help="Relative path to input file containing newline separated questions to group")
    parser.add_argument("--outfile", help="Optional path to output categories to", default="./_grouped_out.txt")
    #_test()
    args = parser.parse_args()
    group(args.path, args.outfile)
    #group("QALD-questions.txt-stripped.txt") #naive_equals)
