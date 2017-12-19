from fuzzywuzzy import fuzz
import string
import spacy


parse_text = spacy.load('en_core_web_lg')

def clean_text(text, option=None):
    text = ' '.join([word for word in text.strip().lower().split()])
    if option == 1:
        text = ''.join([ch for ch in text if ch not in string.punctuation])
    return text


def str_similarity(statement, other_statement):
    print(statement, other_statement)
    ratio_score = fuzz.ratio(statement, other_statement)/100.0
    token_set_ratio_score = fuzz.token_set_ratio(statement, other_statement)/100.0
    return (ratio_score * 0.7) + (token_set_ratio_score * 0.3)
    