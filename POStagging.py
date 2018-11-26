# Install by running:
# pip install spacy
# python -m spacy download en_core_web_sm

import spacy

nlp = spacy.load('en_core_web_sm')
def postagger(nlquestion):
    '''
    Input: Natural language sentence
    Output: A list of tuples (a, b),
    where a is a word in the sentence
    and b is the coarse-grained part-of-speech tag of the word.
    '''
    doc = nlp(nlquestion)

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
    doc = nlp(nlquestion)

    ans = []
    for token in doc:
        ans.append((token.text, token.tag_))

    return ans

def to_tags(question):
    return " ".join(map(lambda x: x[1], postagger(question)))

def _test():
    print(postagger("The quick brown fox jumps over the lazy dog"))
    print(postagger2("The quick brown fox jumps over the lazy dog"))

    print(to_tags("The quick brown fox jumps over the lazy dog"))

if __name__ == "__main__":
    _test()
