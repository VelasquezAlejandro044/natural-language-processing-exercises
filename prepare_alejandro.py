# unit imports 
import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd
from time import strftime

import acquire

#######################################################

def basic_clean(string):
    import unicodedata
    """
    Take in a string and apply some basic text cleaning:
    - Lowercase everything
    - Normalize unicode characters
    - Replace anything that is not a letter, number, whitespace or a single quote.
    """
    # lowercase the string
    string = string.lower()
    # return normal form for the unicode string, encode/remove ascii
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    string = re.sub(r"[^a-z0-9'\s]", '', string) #Replace anything that is not a letter, number, whitespace or a single quote
    return string


def tokenize(string):
    from nltk.tokenize.toktok import ToktokTokenizer
    '''
    This function takes in a string and tokenizes it
    '''
    # create the tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    # use the tokenizer, return as a string
    string = tokenizer.tokenize(string, return_str = True)
    
    return string


def stem(string):
    '''
    This function takes in a string and
    returns a string with stemmed words.
    '''
    # Create porter stemmer
    ps = nltk.porter.PorterStemmer()
    
    # Use 'stemmer' to stem each word in the list of words we created by using '.split'
    stems = [ps.stem(word) for word in string.split()]
    
    # Join our lists of words into a string again and assign to a variable
    string = ' '.join(stems)
    
    return string

def lemmatize(string):
    '''
    This function takes in a string and
    returns a string with lammatized words.
    
    Word **stems** are the base form of a word
    '''
    # Create the lemmatizer.
    wnl = nltk.stem.WordNetLemmatizer()
    
    # Use the lemmatizer on each word in the list of words we created by using split.
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    # Join our list of words into a string again and assign to a variable.
    string = ' '.join(lemmas)
    
    return string

def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    This function takes in a string, optional extra_words and exclude_words parameters
    with default empty lists and returns a string.
    '''
    # Create stopword_list
    stopword_list = stopwords.words('english')
    
    # Remove 'exclude_words' from stopword_list to keep these in text
    stopword_list = set(stopword_list) - set(exclude_words)
    
    # Join 'extra_words' with 'stopword_list'
    stopword_list = stopword_list.union(set(extra_words))

    # Split words in string
    words = string.split()
    
    # Create a list of words from 'string' with stopwords removed and assigned to variable
    filtered_words = [word for word in words if word not in stopword_list]
    
    # Join words in list back into strings and assign to a variable
    string_without_stopwords = ' '.join(filtered_words)
    
    # print count of removed stop worlds 
    print('Removed {} stopwords'.format(len(words) - len(filtered_words)))
    print('---')
    
    return string_without_stopwords

# create a functionnthat would add clean, stemmed, and lammatized columns to the df
def prep_articles_add_to_df(df, extra_words = [], exclude_words = []):
    
    '''
    This function takes in a dataframe, a list of extra words to supplement
    the list of stop words, and a list of words to exclude from the stop words list
    The function returns a dataframe 
    supplemented with clean, stemmed, and lemmatized columns
    '''
    # produce 'original' column
    df = df.rename(columns = {'content': 'original'})
    
    # produce 'clean' column. clean and then tokenize
    df['clean'] = df['original'].apply(basic_clean)\
    .apply(tokenize)\
    .apply(remove_stopwords, extra_words = extra_words, exclude_words = exclude_words)
          
    # produce 'stemmed' column from cleaned column
    df['stemmed'] = df.clean.apply(stem)
    
    # produce 'lemmatizemed' column from cleaned column
    df['lemmatized'] = df.clean.apply(lemmatize)
    
    return df