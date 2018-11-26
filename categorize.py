import subprocess
from pathlib import Path
import argparse
import itertools
import os  # environ
import eq_fns
import warnings
import sys  # exit
from functools import reduce
from to_tree import to_tree, output_tree
import POStagging
import re

# output options
_OUTPUT_QUES = 0
_OUTPUT_TREE = 1
_OUTPUT_BOTH = 2

def load_easyccg_home():
    home = Path(os.environ.get("EASYCCG_HOME", "./easyccg"))
    if "EASYCCG_HOME" not in os.environ:
        warnings.warn("Didn't find EASYCCG_HOME variable, looking for local copy in current directory.", Warning,
                      stacklevel=3)
    return home


'''
Environment Setup
'''
EASYCCG_HOME = load_easyccg_home()
OUT_PATH = Path("/tmp/")


# returns a command arg list which will be used for subprocess
def easyccg_command(file_name=""):
    cmd = "java -jar %s -f %s --model %s" % (EASYCCG_HOME / "easyccg.jar", file_name, EASYCCG_HOME / "model_questions")
    return cmd.split()

def run_easyCCG(input_path):
    with open(posix_path_sup_parser(OUT_PATH / "ccgout.txt"), "w") as outfile:
        subprocess.run(easyccg_command(file_name=input_path), stdout=outfile)

def label(text):
    '''
    text - newline separated sentences to parse
    return - list of string representing the parse of each line
    '''
    # write the input to a temporary file
    tmp_file = OUT_PATH / "labeltmp"
    with open(posix_path_sup_parser(tmp_file), "w") as tmpfile:
        tmpfile.write(text)
    # pass the temp file to easyccg and get output
    with subprocess.Popen(easyccg_command(file_name=tmp_file), stdout=subprocess.PIPE, stderr=open("/dev/null")) as proc:
        #[1::2] - skip parse numbers
        return proc.stdout.read().decode("utf-8").split("\n")[1::2]

def group(file_path, out_path="./_grouped_out.txt", output_switch=0, eq_fn=eq_fns.tree_equals, **kwargs):
    '''
    file_path - path to input
    eq_fn - function taking two trees (and optional kwargs) as input,
    returning True if they are equal and False otherwise. eq_fn should
    be transitive, i.e. if a = b and b = c, then a = c
    file_path - relative (or absolute) path to file containing newline
    separated questions to parse
    kwargs - optional args for eq_fn

    return - a list of categories, where each category is a dict mapping parsed strings to their tree representation
    '''

    # list of dicts {string : tree}
    # categories is a list of dictionaries where each index is a mapping between the parsed question and its tree representation
    # labelled is a dictionary that maps the parsed question to the original question
    categories = []

    with open(file_path) as input_file:
        file_str = input_file.read()

    labelled_list = label(file_str)
    labelled = {l: str(i) + " " + orig for i, (l, orig) in enumerate(zip(labelled_list, file_str.split("\n")))}

    trees = {l: to_tree(l) for l in labelled.keys()}

    for line, tree in trees.items():
        for category in categories:

            # get an arbitrary tree from category
            firstTree = next(iter(category.values()))

            # this category matches, so move on to the next tree
            if eq_fn(tree, firstTree, kwargs['depth']):
                category[line] = tree
                break
        else:
            categories.append({line: tree})

    return categories, labelled

#Function to write the categories to a file
def write_output(categories, labelled, out_path, output_switch, outParams):
    categories.sort(key=len, reverse=True)
    with open(out_path, "w") as grouped_file:
        grouped_file.write("For input %s, %d categories were created from %s questions using depth = %d\n\n" % (outParams[0], len(categories), len(labelled), outParams[1]))
        for n, category in enumerate(categories, start=1):
            questions = (labelled[parse] for parse in category.keys())
            wh_words = {}
            for question in questions:
                word = question.split()[1]
                if word in wh_words.keys():
                    wh_words[word] += 1
                else:
                    wh_words[word] = 1

            wh_words_percentages = []
            for word in wh_words.keys():
                wh_words_percentages.append("%s (%.2f%%)" % (word, wh_words[word] / len(category) * 100))

            grouped_file.write("Category %d: contains %d (%.2f%%) questions with wh-words [%s]\n" % (
                n, len(category), len(category)/len(labelled)*100, ", ".join(wh_words_percentages)))

            if output_switch == _OUTPUT_QUES:
                grouped_file.write("\n".join(str(labelled[parse]) for parse in category.keys()))
                grouped_file.write("\n")

            elif output_switch == _OUTPUT_TREE:
                for root in category.values():
                    output_tree(root, grouped_file)

            elif output_switch == _OUTPUT_BOTH:
                grouped_file.write("\n".join(str(labelled[parse]) for parse in category.keys()))
                grouped_file.write("Common Subtree:\n")
                # naming: including head info TODO delete output
                output_tree(reduce(lambda x, y: x & y, category.values()), grouped_file)

            grouped_file.write("\n")

    print("Created %d categories, written to %s" % (len(categories), out_path))

def posix_path_sup_parser(posix_path):
    # todo decide python version here 3 <= V < 3.6 solved
    if True:
        return str(posix_path)
    return posix_path


# assert that model_questions exists in the easyccg home
def assert_model():
    if not os.path.isdir(posix_path_sup_parser(EASYCCG_HOME / 'model_questions')):
        warnings.warn(
            "model_questions folder doesn't exists in easyccg home directory, please download the model through https://drive.google.com/drive/folders/0B7AY6PGZ8lc-NGVOcUFXNU5VWXc",
            Warning, stacklevel=3)
        sys.exit(1)


def to_pos_tree(text):
    subbed = re.sub(r"POS POS .+?\b", lambda match: r"POS POS "+next(subs), l)
    return to_tree(subbed)


def _test():
    from eq_fns import equals_with_application, _firstWord
    import re
    from POStagging import to_tags


    # t1 = to_tree(label("Which presidents were born in 1945")[0])
    # t2 = to_tree(label("Which presidents were not born in 1945")[0])

    s1 = "Which presidents were born in 1945"
    output_tree(to_pos_tree(s1))
    '''l = label(s1)[0]
    subs = iter(to_tags(s1).split())
    print(l)
    print()
    subbed = re.sub(r"POS POS .+?\b", lambda match: r"POS POS "+next(subs), l)
    print(subbed)
    new_tree = to_tree(subbed)
    output_tree(new_tree)
    print(_firstWord(new_tree))
    # print()
    # print(to_tags(s1))

# //TODO: figure out which part of the string to replace
    output_tree(to_tree(l))
    # for found in re.finditer(r"POS POS (.*\b)", s1):

'''
    # output_tree(t2)

    # print(t1)
    # print(t2)

    # equals_with_application(t1,t2)

if __name__ == "__main__":
    # _test()
    # exit(0)

    assert_model()

    # TODO: take in list of categories and build on that
    parser = argparse.ArgumentParser(description="Group similar questions into categories")
    parser.add_argument("path", help="Relative path to input file containing newline separated questions to group")
    parser.add_argument("--outfile", help="Optional path to output categories to")
    parser.add_argument("-d", "--depth", help="Maximum depth to compare trees at", default=2, type=int)
    parser.add_argument("-o", "--output", help="0:Questions / 1: Trees / 2: Both", default=0, type=int)
    args = parser.parse_args()

    #Process default outfile
    if not args.outfile:
        infilename = args.path.split("/")[-1]
        name = Path(infilename).stem
        args.outfile = "./data/output/%s_grouped_out.txt" % (name)

    categories, labelled = group(args.path, args.outfile, depth=args.depth, output_switch=args.output)
    write_output(categories, labelled, args.outfile, args.output, [args.path, args.depth])

    #TODO: log this?
    # print("Ratio of Categories to Questions:", len(categories) / sum(len(category) for category in categories))

    if len(categories) / sum(len(category) for category in categories) > .5:
        warnings.warn(
            "Warning: Categories are very small. Consider using a smaller depth argument to group more questions together.",
            Warning, stacklevel=3)
