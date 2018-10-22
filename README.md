# EasyCCGTrees
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
