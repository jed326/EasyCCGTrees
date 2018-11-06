#!/bin/bash
python3 groupLines.py --outfile data/output/_grouped_out_questions.txt --output 0 data/input/QALD-questions-stripped.txt
python3 groupLines.py --outfile data/output/_grouped_out_trees.txt --output 1 data/input/QALD-questions-stripped.txt
python3 groupLines.py --outfile data/output/_grouped_out_both.txt --output 2 data/input/QALD-questions-stripped.txt
