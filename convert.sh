#!/bin/bash

# settings
EASYCCG_HOME="./easyccg"
input_file="QALD-questions.txt"
to_tree_command="python3 to_tree.py"
ignore_col=1

while getopts "hi:" o; do
	case $o in
		i)
			ignore_col=`expr ${OPTARG} + 1`
			;;
		h)
			echo "usage: ./convert [-i1]"
			exit
			;;
		*)
			echo "usage: ./convert [-i1]"
			exit
			;;
	esac
done

if [ $ignore_col -eq 1 ]; then
	echo "Using $(tput setaf 1)every column$(tput sgr 0) of file ${input_file} as input"
else
	echo "Ignoring $(tput setaf 1)$(expr $ignore_col - 1) column $(tput sgr 0) of file $of file ${input_file} as input"
fi


cat ${input_file}| cut -d' ' -f${ignore_col}- | java -jar ${EASYCCG_HOME}/easyccg.jar --model ${EASYCCG_HOME}/model_questions -s -r S[q] S[qem] S[wq] | while read id_line;read parse_line
do
	tree=`echo "$parse_line" | eval ${to_tree_command}`
	line_num=`echo $id_line | cut -d'=' -f2`
	question=`sed "${line_num}!d" ${input_file} | cut -d' ' -f${ignore_col}-`
	printf "%s: %s\n%s\n" $line_num "$question" "$tree"
done
