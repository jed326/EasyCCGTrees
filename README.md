# EasyCCGTrees
This repository was created for the Honors Option for Computer Science 442 at The Pennsylvania State University.   
Authors: Steven Fontanella, Jay Deng, ZhaoHong Lu, QiYi Shan

### Table of Contents
* [About](https://github.com/jed326/EasyCCGTrees#About)
* [Setup Tutorial](https://github.com/jed326/EasyCCGTrees#Setup-Tutorial)
* [Data](https://github.com/jed326/EasyCCGTrees#data)
* [EasyCCG Submodule](https://github.com/jed326/EasyCCGTrees#EasyCCG-Submodule)
* [categorize.py](https://github.com/jed326/EasyCCGTrees#categorize.py)
* [convert.sh & to_tree.py](https://github.com/jed326/EasyCCGTrees#convert.sh-&-to_tree.py)

## About
This repository can be used to categorize questions based upon their CCG parses from EasyCCG.

## Setup Tutorial
####SETUP INSTRUCTIONS COMING SOON

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
Pre-trained modules can be downloaded here: <https://drive.google.com/drive/folders/0B7AY6PGZ8lc-NGVOcUFXNU5VWXc>   
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
                        0:Questions / 1: Trees / 2: Both
```

## convert.sh & to_tree.py
to_tree.py natively receives a easyccg output from stdin and writes the corresponding tree string to stdout

convert.sh uses to_tree function to help batch converting questions to tree form
```bash
./convert data/input/QALD-questions-stripped.txt > output.txt
# or use -i to ignore 1 column per line
./convert -i1 data/input/QALD-questions.txt > output.txt
```

### batch_categorize.sh
helper script that export all three types of categorized result to folder: data/output
