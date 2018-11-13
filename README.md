# EasyCCGTrees

## Table of Contents
* [About](https://github.com/jed326/EasyCCGTrees#About)
* [Setup Tutorial](https://github.com/jed326/EasyCCGTrees#Setup-Tutorial)
* [Data](https://github.com/jed326/EasyCCGTrees#data)
* [EasyCCG Submodule](https://github.com/jed326/EasyCCGTrees#EasyCCG-Submodule)
* [ETE_Trees](https://github.com/jed326/EasyCCGTrees#ETE_Trees)
* [categorize.py](https://github.com/jed326/EasyCCGTrees#categorizepy)
* [convert.sh & to_tree.py](https://github.com/jed326/EasyCCGTrees#convertsh--to_treepy)
* [batch_categorize.sh](https://github.com/jed326/EasyCCGTrees#batch_categorizesh)

## About
This repository can be used to categorize questions based upon their CCG parses from EasyCCG.
This repository was created for the Honors Option for Computer Science 442 at The Pennsylvania State University.   
Authors: Steven Fontanella, Jay Deng, ZhaoHong Lu, QiYi Shan

## Setup Tutorial
For instructions on cloning this repository along with it's submodule, reference [EasyCCG Submodule](https://github.com/jed326/EasyCCGTrees#EasyCCG-Submodule).   
For this project, the pre-trained module used in development is `model_questions`.

#### Input Requirements:
The `categorize.py` script requires a path to an input file that contains lines of questions without line numbers. The python script `data/clean.py` contains a function that will strip line numbers from an input file.

#### Categorizing Questions:
For instructions on running the categorization script `categorize.py`, reference [categorize.py](https://github.com/jed326/EasyCCGTrees#categorizepy).
If an `--outfile` parameter is not provided, `categorize.py` will default the output to `data/output/_<inputfile>_grouped_out.txt`.

#### Output:
The contents of the output file will depend on what option is given to the `-o` flag of `categorize.py`.   
Option | Output Description
0 | The output will contain only the categorized questions.
1 | The output will contain only the categorized CCG trees.
2 | The output will contain all of the categorized questions as well as their common CCG subtree.

## [Data](https://github.com/jed326/EasyCCGTrees/tree/master/data)
This directory contains all of the data files for both inputting questions to be categorized and outputting questions that have been categorized.   
This directory also contains a script `clean.py` which contains different question file processing functions.

## [EasyCCG Submodule](https://github.com/mikelewis0/easyccg/tree/e42d58e08eb2a86593d52f730c5afe222e939781)
EasyCCG is a CCG parser created by Mike Lewis. It is added as a submodule to this repository.   

#### 1. To include EasyCCG when cloning, use the command:
```bash
git clone --recursive git@github.com:jed326/EasyCCGTrees.git
```
#### 2. To get EasyCCG after cloning, use the commands:
```bash
git submodule init
git submodule update
```
EasyCCG requires a model in order to run. Fortunately, the author of EasyCCG has provided pre-trained modules.   
Pre-trained modules can be downloaded here: <https://drive.google.com/drive/folders/0B7AY6PGZ8lc-NGVOcUFXNU5VWXc>   
After the modules have been downloaded, they should be placed in the `easyccg/` directory.   
For more detailed setup instructions, reference the EasyCCG repository.

#### EasyCCG Usage:
To parse questions into text form:

```bash
java -jar $EASYCCG_HOME/easyccg.jar -f path/to/input  --model $EASYCCG_HOME/model_questions [> outfile.txt]
```

To output trees to html:

```bash
java -jar $EASYCCG_HOME/easyccg.jar -f path/to/input  --model $EASYCCG_HOME/model_questions -o html [> outfile.txt]
```

## ETE_Trees
ETE is a python library that can be used to visualize and print out python tree structures. Specifically this can be used to save trees to .png files.   
Instructions on how to use ETE can be found in the ETE_Trees directory.   

## categorize.py
This file is the primary script for this project. Usage is as follows:      
```
usage: python3 categorize.py [-h] [--outfile OUTFILE] [-d DEPTH] [-o OUTPUT] path

Group similar questions into categories

positional arguments:
  path                  Relative path to input file containing newline
                        separated questions to group

optional arguments:
  -h, --help            show this help message and exit
  --outfile OUTFILE     Optional path to output categories to
  -d DEPTH, --depth DEPTH
                        Maximum depth to compare trees at
  -o OUTPUT, --output OUTPUT
                        0: Questions Only / 1: Trees Only / 2: Questions and Common Subtree
```

## convert.sh & to_tree.py
to_tree.py natively receives a easyccg output from stdin and writes the corresponding tree string to stdout

convert.sh uses to_tree function to help batch converting questions to tree form
```bash
./convert data/input/QALD-questions-stripped.txt > output.txt
# or use -i to ignore 1 column per line
./convert -i1 data/input/QALD-questions.txt > output.txt
```

## batch_categorize.sh
This is a helper script that exports all three types of categorized results to folder: `data/output`   
The types are broken down here: [Output](https://github.com/jed326/EasyCCGTrees#output)
