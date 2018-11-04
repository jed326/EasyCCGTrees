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

## data

Instructions on how to use ETE can be found in the ETE_Trees directory.

## EasyCCG Usage
To parse into text form:

```
java -jar $EASYCCG_HOME/easyccg.jar -f path/to/input  --model $EASYCCG_HOME/model_questions [> outfile.txt]
```

To output trees to html:

```
java -jar $EASYCCG_HOME/easyccg.jar -f path/to/input  --model $EASYCCG_HOME/model_questions -o html [> outfile.txt]
```
