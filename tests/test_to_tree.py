import unittest
from categorize import *
from to_tree import *

# python -m unittest

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_label(self):
        test_cases = ["What presidents were born in 1945?",
                      "Which presidents were born in 1946",
                      "Which presidents were not born in 1945",
                      ]
        labels = label("\n".join(test_cases))
        answer = ['(<T S[wq] 0 2> (<T S[wq]/(S[dcl]\\NP) 0 2> (<L (S[wq]/(S[dcl]\\NP))/N POS POS What (S[wq]/(S[dcl]\\NP))/N>) (<L N POS POS presidents N>) ) (<T S[dcl]\\NP 0 2> (<L (S[dcl]\\NP)/(S[pss]\\NP) POS POS were (S[dcl]\\NP)/(S[pss]\\NP)>) (<T S[pss]\\NP 0 2> (<L S[pss]\\NP POS POS born S[pss]\\NP>) (<T (S\\NP)\\(S\\NP) 0 2> (<L ((S\\NP)\\(S\\NP))/NP POS POS in ((S\\NP)\\(S\\NP))/NP>) (<T NP 0 1> (<L N POS POS 1945? N>) ) ) ) ) ) ', '(<T S[wq] 0 2> (<T S[wq]/(S[dcl]\\NP) 0 2> (<L (S[wq]/(S[dcl]\\NP))/N POS POS Which (S[wq]/(S[dcl]\\NP))/N>) (<L N POS POS presidents N>) ) (<T S[dcl]\\NP 0 2> (<L (S[dcl]\\NP)/(S[pss]\\NP) POS POS were (S[dcl]\\NP)/(S[pss]\\NP)>) (<T S[pss]\\NP 0 2> (<L S[pss]\\NP POS POS born S[pss]\\NP>) (<T (S\\NP)\\(S\\NP) 0 2> (<L ((S\\NP)\\(S\\NP))/NP POS POS in ((S\\NP)\\(S\\NP))/NP>) (<T NP 0 1> (<L N POS POS 1946 N>) ) ) ) ) ) ', '(<T S[wq] 0 2> (<T S[wq]/(S[dcl]\\NP) 0 2> (<L (S[wq]/(S[dcl]\\NP))/N POS POS Which (S[wq]/(S[dcl]\\NP))/N>) (<L N POS POS presidents N>) ) (<T S[dcl]\\NP 0 2> (<T (S[dcl]\\NP)/(S[pss]\\NP) 0 2> (<L (S[dcl]\\NP)/(S[pss]\\NP) POS POS were (S[dcl]\\NP)/(S[pss]\\NP)>) (<L (S\\NP)\\(S\\NP) POS POS not (S\\NP)\\(S\\NP)>) ) (<T S[pss]\\NP 0 2> (<L S[pss]\\NP POS POS born S[pss]\\NP>) (<T (S\\NP)\\(S\\NP) 0 2> (<L ((S\\NP)\\(S\\NP))/NP POS POS in ((S\\NP)\\(S\\NP))/NP>) (<T NP 0 1> (<L N POS POS 1945 N>) ) ) ) ) ) ']
        self.assertTrue(labels)

    # todo
    def test_node_from_ccg(self):
        labels = ['(<T S[wq] 0 2> (<T S[wq]/(S[dcl]\\NP) 0 2> (<L (S[wq]/(S[dcl]\\NP))/N POS POS What (S[wq]/(S[dcl]\\NP))/N>) (<L N POS POS presidents N>) ) (<T S[dcl]\\NP 0 2> (<L (S[dcl]\\NP)/(S[pss]\\NP) POS POS were (S[dcl]\\NP)/(S[pss]\\NP)>) (<T S[pss]\\NP 0 2> (<L S[pss]\\NP POS POS born S[pss]\\NP>) (<T (S\\NP)\\(S\\NP) 0 2> (<L ((S\\NP)\\(S\\NP))/NP POS POS in ((S\\NP)\\(S\\NP))/NP>) (<T NP 0 1> (<L N POS POS 1945? N>) ) ) ) ) ) ', '(<T S[wq] 0 2> (<T S[wq]/(S[dcl]\\NP) 0 2> (<L (S[wq]/(S[dcl]\\NP))/N POS POS Which (S[wq]/(S[dcl]\\NP))/N>) (<L N POS POS presidents N>) ) (<T S[dcl]\\NP 0 2> (<L (S[dcl]\\NP)/(S[pss]\\NP) POS POS were (S[dcl]\\NP)/(S[pss]\\NP)>) (<T S[pss]\\NP 0 2> (<L S[pss]\\NP POS POS born S[pss]\\NP>) (<T (S\\NP)\\(S\\NP) 0 2> (<L ((S\\NP)\\(S\\NP))/NP POS POS in ((S\\NP)\\(S\\NP))/NP>) (<T NP 0 1> (<L N POS POS 1946 N>) ) ) ) ) ) ', '(<T S[wq] 0 2> (<T S[wq]/(S[dcl]\\NP) 0 2> (<L (S[wq]/(S[dcl]\\NP))/N POS POS Which (S[wq]/(S[dcl]\\NP))/N>) (<L N POS POS presidents N>) ) (<T S[dcl]\\NP 0 2> (<T (S[dcl]\\NP)/(S[pss]\\NP) 0 2> (<L (S[dcl]\\NP)/(S[pss]\\NP) POS POS were (S[dcl]\\NP)/(S[pss]\\NP)>) (<L (S\\NP)\\(S\\NP) POS POS not (S\\NP)\\(S\\NP)>) ) (<T S[pss]\\NP 0 2> (<L S[pss]\\NP POS POS born S[pss]\\NP>) (<T (S\\NP)\\(S\\NP) 0 2> (<L ((S\\NP)\\(S\\NP))/NP POS POS in ((S\\NP)\\(S\\NP))/NP>) (<T NP 0 1> (<L N POS POS 1945 N>) ) ) ) ) ) ']
        trees = [CCGNode.from_ccg(l) for l in labels]
        # print(trees)
        # tree node compare
