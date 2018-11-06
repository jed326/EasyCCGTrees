import subprocess
import pathlib
import argparse
import itertools
import os  # environ
import eq_fns
import warnings
import sys  # exit
from to_tree import to_tree, output_tree


# REQUIRED: Input path argument
# OPTIONAL: ouput path argument


def load_easyccg_home():
    home = pathlib.Path(os.environ.get("EASYCCG_HOME", "./easyccg"))
    if "EASYCCG_HOME" not in os.environ:
        warnings.warn("Didn't find EASYCCG_HOME variable, looking for local copy in current directory.", Warning,
                      stacklevel=3)
    return home


'''
Environment Setup
'''
EASYCCG_HOME = load_easyccg_home()
OUT_PATH = pathlib.Path("/tmp/")


# returns a command arg list which will be used for subprocess
def easyccg_command(file_name=""):
    cmd = "java -jar %s -f %s --model %s" % (EASYCCG_HOME / "easyccg.jar", file_name, EASYCCG_HOME / "model_questions")
    return cmd.split()


def run_easyCCG(input_path):
    with open(posix_path_sup_parser(OUT_PATH / "ccgout.txt"), "w") as outfile:
        subprocess.run(easyccg_command(file_name=input_path), stdout=outfile)


# used to remove id's in the first column
def remove_IDs():
    with open(posix_path_sup_parser(OUT_PATH / "ccgout.txt")) as origfile:
        with open(posix_path_sup_parser(OUT_PATH / "ccgout_stripped.txt"), "w") as newfile:
            for count, line in enumerate(origfile):
                if count % 2 == 1:
                    print(line.rstrip(), file=newfile)


# input: question text
# output: list of labels for the text
def label(text):
    # write the input to a temporary file
    tmp_file = OUT_PATH / "labeltmp"
    with open(posix_path_sup_parser(tmp_file), "w") as tmpfile:
        tmpfile.write(text)
    # pass the temp file to easyccg and get output
    with subprocess.Popen(easyccg_command(file_name=tmp_file), stdout=subprocess.PIPE) as proc:
        return proc.stdout.read().decode("utf-8").split("\n")[1::2]


def group(file_path, out_path="./_grouped_out.txt", eq_fn=eq_fns.tree_equals, output_switch=0, **kwargs):
    # list of dicts {string : tree}
    # categories is a list of dictionaries
    # each index is a mapping between the parsed question and its tree representation
    # labelled is a dictionary that maps the parsed question to the original question
    categories = []
    labelled = {}

    with open(file_path) as input_file:
        # TODO: don't read file twice; store in variable instead
        labelled_list = label(input_file.read())

        input_file.seek(0)
        # original_questions = [label,orig for label,orig in zip(labelled_list, input_file)]
        # labelled = {}
        # for orig in original_questions:
        #     labelled.update
        labelled = {l: str(i) + " " + orig for i, (l, orig) in enumerate(zip(labelled_list, input_file))}

    # labelled = labelled[:20]
    # print(labelled)

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

            wh_words_percentages = []
            for word in wh_words.keys():
                wh_words_percentages.append("%s (%.2f%%)" % (word, wh_words[word] / len(category) * 100))

            grouped_file.write("Category %d: contains %d questions with wh-words [%s]\n" % (
                n, len(category), ", ".join(wh_words_percentages)))

            if output_switch == 0:
                grouped_file.write("".join(str(labelled[parse]) for parse in category.keys()))

            elif output_switch == 1:
                for root in category.values():
                    output_tree(root, grouped_file)

            elif output_switch == 2:
                grouped_file.write("".join(str(labelled[parse]) for parse in category.keys()))
                # naming: including head info TODO delete output
                output_tree(next(iter(category.values())), grouped_file, limit=kwargs['depth'] + 1)

            grouped_file.write("\n")
            n += 1

    print("Created %d categories, written to %s" % (len(categories), out_path))

    return categories


def posix_path_sup_parser(posix_path):
    # todo decide python version here 3 <= V < 3.6 solved 
    if True:
        return str(posix_path)
    return posix_path


# assert that model_questions exists in the easyccg home
def assert_model():
    if not os.path.isdir(EASYCCG_HOME / 'model_questions'):
        warnings.warn(
            "model_questions folder doesn't exists in easyccg home directory, please download the model through https://drive.google.com/drive/folders/0B7AY6PGZ8lc-NGVOcUFXNU5VWXc",
            Warning, stacklevel=3)


if __name__ == "__main__":
    assert_model()
    #####
    # TODO: add flags for printing tagged form or normal form; possibly have common tree at the top of each category
    # or print out list of categories,where each category is just one tree
    # or output parameter for depth

    # take in list of categories
    parser = argparse.ArgumentParser(description="Group similar questions into categories")
    parser.add_argument("path", help="Relative path to input file containing newline separated questions to group")
    parser.add_argument("--outfile", help="Optional path to output categories to", default="./_grouped_out.txt")
    parser.add_argument("-d", "--depth", help="Maximum depth to compare trees at", default=2, type=int)
    parser.add_argument("-o", "--output", help="0:Questions / 1: Trees / 2: Both", default=0, type=int)
    args = parser.parse_args()

    categories = group(args.path, args.outfile, depth=args.depth, output_switch=args.output)

    print(len(categories))

    print(len(categories) / sum(len(category) for category in categories))
    if len(categories) / sum(len(category) for category in categories) > .5:
        warnings.warn(
            "Warning: Categories are very small. Consider using a smaller depth argument to group more questions together.",
            Warning, stacklevel=3)
