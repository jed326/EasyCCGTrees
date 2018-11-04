# EasyCCGTrees
This repository can be used to group questions parsed with EasyCCG.   
The main components are:   
1. Data Cleaning
2. data
3. easyccg
4. ETE_Trees
5. groupLines.py
6. convert.sh & to_tree.py

## [Data Cleaning](https://github.com/jed326/EasyCCGTrees/tree/stats/Data%20Cleaning)
##### Contains scripts for parsing data files

## data
##### Contains the input and output data files

## [EasyCCG](https://github.com/mikelewis0/easyccg/tree/e42d58e08eb2a86593d52f730c5afe222e939781)
EasyCCG is a CCG parser created by Mike Lewis. It is added as a submodule to this repository.   
To include EasyCCG when cloning, use the command:
```
git clone --recursive
```
Pre-trained modules can be downloaded here: [https://drive.google.com/drive/folders/0B7AY6PGZ8lc-NGVOcUFXNU5VWXc]   
For more detailed setup instructions, reference the EasyCCG repository.

### EasyCCG Usage:
To parse into text form:

```
java -jar $EASYCCG_HOME/easyccg.jar -f path/to/input  --model $EASYCCG_HOME/model_questions [> outfile.txt]
```

To output trees to html:

```
java -jar $EASYCCG_HOME/easyccg.jar -f path/to/input  --model $EASYCCG_HOME/model_questions -o html [> outfile.txt]
```



Instructions on how to use ETE can be found in the ETE_Trees directory.

## EasyCCG Usage
