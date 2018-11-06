import subprocess
import pathlib
import argparse
import itertools
import os #environ
import eq_fns
import sys #exit
from to_tree import to_tree, output_tree


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
    with open(posix_path_sup_parser(OUT_PATH / "ccgout.txt"), "w") as outfile:
        subprocess.run(["java", "-jar", str(EASYCCG_HOME / "easyccg.jar"), "-f", input_path,
                        "--model", str(EASYCCG_HOME / "model_questions")],
                       stdout=outfile)


def remove_IDs():
    with open(posix_path_sup_parser(OUT_PATH / "ccgout.txt")) as origfile:
        with open(posix_path_sup_parser(OUT_PATH / "ccgout_stripped.txt"), "w") as newfile:
            for count, line in enumerate(origfile):
                if count % 2 == 1:
                    print(line.rstrip(), file=newfile)



def label(text):
    with open(posix_path_sup_parser(OUT_PATH / "_labeltmp"), "w") as tmpfile:
        tmpfile.write(text)
    with subprocess.Popen(["java", "-jar", str(EASYCCG_HOME / "easyccg.jar"), "-f", "/tmp/_labeltmp",
                           "--model", str(EASYCCG_HOME / "model_questions")], stdout=subprocess.PIPE) as proc:
        return proc.stdout.read().decode("utf-8").split("\n")[1::2]


'''
    eq_fn - function taking two trees (and optional kwargs) as input,
    returning True if they are equal and False otherwise. eq_fn should
    be transitive, i.e. if a = b and b = c, then a = c

    file_path - relative (or absolute) path to file containing newline
    separated questions to parse

    output_switch - 0. questions only / 1. tree only / 2. both 

    kwargs - extra args for eq_fn
'''
def group(file_path, out_path="./_grouped_out.txt", eq_fn=eq_fns.tree_equals, output_switch=0, **kwargs):
    #list of dicts {string : tree}
    # categories is a list of dictionaries
    # each index is a mapping between the parsed question and its tree representation
    # labelled is a dictionary that maps the parsed question to the original question
    categories = []
    labelled = {}

    with open(file_path) as input_file:
        #TODO: don't read file twice; store in variable instead
        labelled_list = label(input_file.read())

        input_file.seek(0)
        # original_questions = [label,orig for label,orig in zip(labelled_list, input_file)]
        # labelled = {}
        # for orig in original_questions:
        #     labelled.update
        labelled = {label: str(i) + " " + orig for i, (label, orig) in enumerate(zip(labelled_list, input_file))}

    # labelled = labelled[:20]
    # print(labelled)

    trees = {label: to_tree(label) for label in labelled.keys()}
    # trees = list(map(labelled, to_tree))
    # print("\n".join(labelled[:10]))

    for line, tree in trees.items():
        for category in categories:

            # get an arbitrary tree from category
            firstTree = next(iter(category.values()))

            #this category matches, so move on to the next tree
            if eq_fn(tree, firstTree, kwargs['depth']):
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
                    wh_words.update({word: 1})
            # print(wh_words)

            wh_words_percentages = []
            for word in wh_words.keys():
                wh_words_percentages.append("%s (%.2f%%)" % (word, wh_words[word] / len(category) * 100))

            # print(wh_words_percentages)

            grouped_file.write("Category %d: contains %d questions with wh-words [%s]\n" % (
                n, len(category), ", ".join(wh_words_percentages)))

            if output_switch == 0:
                grouped_file.write("".join(str(labelled[parse]) for parse in category.keys()))
                
            elif output_switch == 1:
                for root in category.values():
                    output_tree(root, grouped_file)

            elif output_switch == 2:
                grouped_file.write("".join(str(labelled[parse]) for parse in category.keys()))
                output_tree(next(iter(category.values())), grouped_file, limit=kwargs['depth'])

            grouped_file.write("\n")
            n += 1


    print("Created %d categories, written to %s" % (len(categories), out_path))

    return categories

def posix_path_sup_parser(posix_path):
    # todo decide python version here 3 <= V < 3.6 solved 
    if True:
        return str(posix_path)
    return posix_path

def _test():
    tree2 = to_tree(label("How do commercial jets fly"))
    tree1 = to_tree(label("How do airplanes fly"))

    # output_tree(tree1)

    from eq_fns import _tree_weight
    # print(_tree_weight(tree1))
    # output_tree(tree1)
    eq_fns.equals_with_application(tree1, tree2)
    output_tree(tree1)


if __name__ == "__main__":
    #_test()
    #sys.exit(0)
    #TODO: add flags for printing tagged form or normal form; possibly have common tree at the top of each category
    #or print out list of categories,where each category is just one tree
    #or output
    #parameter for depth
    #take in list of categories
    parser = argparse.ArgumentParser(description="Group similar questions into categories")
    parser.add_argument("path", help="Relative path to input file containing newline separated questions to group")
    parser.add_argument("--outfile", help="Optional path to output categories to", default="./_grouped_out.txt")
    parser.add_argument("-d", "--depth", help="Maximum depth to compare trees at", default=2, type=int)
    parser.add_argument("-o", "--output", help="0:Questions / 1: Trees / 2: Both", default=0, type=int)
    args = parser.parse_args()


    #fns = eq_fns.__all__
    #for fn in fns:
    #    print(fn.__name__)
    categories = group(args.path, args.outfile, depth=args.depth, output_switch=args.output)
    print(len(categories))

    print(len(categories) / sum( len(category) for category in categories))
    if len(categories) / sum( len(category) for category in categories) > .5:
        print("Warning: Categories are very small. Consider using a smaller depth argument to group more questions together.")
