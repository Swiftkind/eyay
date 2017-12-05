from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS as stopwords 
from fuzzywuzzy import fuzz
import string
import spacy


parse_text = spacy.load('en_core_web_sm')

def remove_stopwords(text):
    return ' '.join([word for word in text.split() if word not in stopwords])


def clean_text(text):     
    text = ' '.join([word for word in text.strip().lower().split()])
    text = ''.join([ch for ch in text if ch not in string.punctuation])
    return text if len(remove_stopwords(text)) == 0 else remove_stopwords(text)


def str_similarity(statement, other_statement):
    print(statement, other_statement)
    return fuzz.token_set_ratio(statement, other_statement)/100.0
