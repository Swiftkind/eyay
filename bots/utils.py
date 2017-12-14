from fuzzywuzzy import fuzz
import string
import spacy


parse_text = spacy.load('en_core_web_lg')

def clean_text(text):     
    text = ' '.join([word for word in text.strip().lower().split()])
    text = ''.join([ch for ch in text if ch not in string.punctuation])
    return text


def str_similarity(statement, other_statement):
    print(statement, other_statement)
    return fuzz.token_set_ratio(statement, other_statement)/100.0
