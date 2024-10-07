import spacy
import re
import os
import tqdm
import pandas as pd
from functools import reduce
from spacy.lang.en.stop_words import STOP_WORDS as spacy_stop_words
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords as nltk_stop_words

try:
    from src import config
    from src import utils
except:
    import config
    import utils

logger = utils.logger

STOP_WORDS = set(spacy_stop_words).union(set(nltk_stop_words.words("english")))
SPACY_TOKENIZER = spacy.load('en_core_web_sm')

def separate_capitalilzed_words(text:str)->str:
    """
    Introduce space before each capital letter
    Example: "ThisIsAWord" -> "This Is A Word"
    :param text: str
    :return: str
    """
    assert isinstance(text, str)
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    return text

def lower_case(text:str)->str:
    """
    Lower case text
    :param text: str
    :return: str
    """
    assert isinstance(text, str)
    text = text.lower()
    return text

def fix_white_space(text:str)->str:
    """
    Fix white space
    :param text: str
    :return: str
    """
    assert isinstance(text, str)
    text = "\n".join(" ".join(text.split()).split("\n"))
    return text

def text_to_paragraphs(text:str)->list:
    """
    Convert text to paragraphs
    :param text: str
    :return: list
    """
    if not isinstance(text, str):
        return []
    paragraphs = list(filter(lambda x: x!="", text.split("\n")))
    return paragraphs

def text_to_sentences(text:str)->list:
    """
    Convert text to sentences
    :param text: str
    :return: list
    """
    if not isinstance(text, str):
        return []
    sentences = SPACY_TOKENIZER(text).sents
    sentences = [str(sentence) for sentence in sentences]
    return sentences

def remove_non_alphanumeric(text:str)->str:
    """
    Remove everything except alphanumeric characters and spaces
    :param text: str
    :return: str
    """
    assert isinstance(text, str)
    pattern = '[^a-zA-Z0-9%\ \n]+'
    return re.sub(pattern, '', text)

def remove_digits(text:str)->str:
    """
    Remove digits
    :param text: str
    :return: str
    """
    assert isinstance(text, str)
    text = re.sub(r'\d+', '', text)
    return text

def remove_stop_words(text:str)->str:
    """
    Remove stop words
    :param text: str
    :return: str
    """
    assert isinstance(text, str)
    text = " ".join([word for word in text.lower().split() if word not in STOP_WORDS])
    return text

def spacy_tokenize(text:str)->list:
    """
    Tokenize text
    :param text: str
    :return: list
    """
    assert isinstance(text, str)
    return " ".join([token.text for token in SPACY_TOKENIZER(text)])

def spacy_lemmatize(text)->str:
    """
    Lemmatize text to find the root of the word
    :param text: str
    :return: str
    """
    assert isinstance(text, str)
    text = " ".join([token.lemma_ for token in SPACY_TOKENIZER(text)])
    return text

def preprocess_text(text:str)->str:
    """
    Preprocess text
    :param text: str
    :return: str
    """
    text = str(text)
    text = separate_capitalilzed_words(text)
    text = lower_case(text)
    text = remove_non_alphanumeric(text)
    text = remove_digits(text)
    text = fix_white_space(text)
    text = remove_stop_words(text)
    text = spacy_tokenize(text)
    text = spacy_lemmatize(text)
    return text

if __name__ == "__main__":
    # # output_filename = utils.get_raw_data_from_aws_mongo()
    # output_filename = "data/raw/raw.csv"
    # print(preprocess_data(output_filename, sample_size=50, section_by=config.TEXT_SECTION_TYPE, input_types=config.TRAIN_DATA_INPUT_TYPES))
    text = "Aspiring Human Resources Manager | Graduating May 2020 | Seeking an Entry-Level Human Resources Position in St. Louis"
    r = preprocess_text(text)
    print(r)