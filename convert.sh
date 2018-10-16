#!/bin/bash

# settings
EASYCCG_HOME="/Users/seancheey/Desktop/-NLP/easyccg-0.2"
input_file="QALD-questions.txt"
output_file="output.txt"
to_tree_command="./to_tree.py"

cat ${input_file}| while read line; do
	line_num=`echo $line | cut -d' ' -f1`
	question=`echo $line | cut -d' ' -f2-`
	ans=$(printf "${question}" | java -jar ${EASYCCG_HOME}/easyccg.jar --model ${EASYCCG_HOME}/model_questions -s -r S[q] S[qem] S[wq] | eval ${to_tree_command})
	printf "%s, %s:\n%s\n" $line_num "$question" "$ans"
	printf "%s, %s:\n%s\n" $line_num "$question" "$ans" >> $output_file
done
