# Install by running:
# pip install spacy
# python -m spacy download en_core_web_sm

import spacy

def postagger(nlquestion):
    '''
    Input: Natural language sentence
    Output: A list of tuples (a, b),
    where a is a word in the sentence
    and b is the coarse-grained part-of-speech tag of the word.
    '''
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(unicode(nlquestion))
    
    ans = []
    for token in doc:
        ans.append((token.text, token.pos_))
    
    return ans
    
def postagger2(nlquestion):
    '''
    Input: Natural language sentence
    Output: A list of tuples (a, b),
    where a is a word in the sentence
    and b is the fine-grained part-of-speech tag of the word.
    '''
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(unicode(nlquestion))
    
    ans = []
    for token in doc:
        ans.append((token.text, token.tag_))
    
    return ans