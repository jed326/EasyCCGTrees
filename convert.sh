#!/bin/bash

# settings
EASYCCG_HOME="./easyccg"
input_file="QALD-questions.txt"
to_tree_command="python to_tree.py"
ignore_line=1

while getopts "hi:" o; do
	case $o in
		i)
			ignore_line=`expr ${OPTARG} + 1`
			;;
		h)
			echo "usage: ./convert [-i 1]"
			exit
			;;
		*)
			echo "usage: ./convert [-i 1]"
			exit
			;;
	esac
done

tree_string=`cat ${input_file}| cut -d' ' -f${ignore_line}- | java -jar ${EASYCCG_HOME}/easyccg.jar --model ${EASYCCG_HOME}/model_questions -s -r S[q] S[qem] S[wq]`

echo "${tree_string}"| while read id_line;read parse_line
do
	tree=`echo "$parse_line" | eval ${to_tree_command}`
	line_num=`echo $id_line | cut -d'=' -f2`
	printf "%s:\n%s\n" $line_num "$tree"
done
