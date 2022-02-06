import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os
from time import strftime
###############################################################################

def get_blog_articles(url):
    '''
    Function takes in a url and returns a dictionary with title and body of it
    '''
    
    # create a user-agent header 
    headers = {'User-Agent': 'Codeup Data Science'} 
    
    # make the request
    response = get(url, headers=headers)
    
    # turn response itno html text to ensure you have an html page work with
    html = response.text
    
    # use BeautifulSoup to parse the HTML into a variable ('soup').
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # get the titile of the article usnig soup.title.string
    title = soup.title.string
    # published date
    published = soup.select_one('.published').text
    # boddy of the article
    article = soup.select_one(".entry-content").text.strip()
    
    # append the elements to the dictionary
    return {'title': title, 'content': article, 'published_date':published}

  
def title_contetn_date_df():
    '''
    # run a for loop in list comprehension to convert in a dataframe with 
    the title of the blog post, the blog's content and the date it was poublished
    '''
    title_contetn_date_df = pd.DataFrame(get_blog_articles(url) for url in blog_url)
    return title_contetn_date_df

def get_card_list():
    cards = soup.select('.news-card')
    #loop creates a list of cards
    list_of_cards=[card
    for card in crads:
        
    
    #create alistof crds to return 

def parse_news_card(card):
    'Given a news card object, returns a dictionary of the relevant information.'
    card_title = card.select_one('.news-card-title')
    output = {}
    output['title'] = card.find('span', itemprop = 'headline').text
    output['author'] = card.find('span', class_ = 'author').text
    output['content'] = card.find('div', itemprop = 'articleBody').text
    output['date'] = card.find('span', clas ='date').text
    return output


def parse_inshorts_page(url='https://www.inshorts.com/en/read/'):
    '''Given a url, returns a dataframe where each row is a news article from the url.
    Infers the category from the last section of the url.'''
    category = url.split('/')[-1]
    response = requests.get(url, headers={'user-agent': 'Codeup DS'})
    soup = BeautifulSoup(response.text)
    cards = soup.select('.news-card')
    df = pd.DataFrame([parse_news_card(card) for card in cards])
    df['category'] = category
    return df

def get_inshorts_articles():
    '''
    Returns a dataframe of news articles from the business, sports, technology, and 
    entertainment sections of inshorts.
    '''
    url = 'https://inshorts.com/en/read/'
    categories = ['business', 'sports', 'technology', 'entertainment']
    df = pd.DataFrame()
    
    # loops on the categories
    for cat in categories:
        df = pd.concat([df, pd.DataFrame(parse_inshorts_page(url + cat))])
    df = df.reset_index(drop=True)
    return df


def df_to_json():
    '''
    Uses the get_inshorts_articles to create DF and saves it locally as a json file
    it uses the date to ensure that we keep daily record of when record was created
    '''
    from time import strftime # datetime to string using
    
    # creates a time string 
    today = strftime('%Y-%m-%d')
    
    # saves ds to jason using a predifine functtion'get_inshorts_articles'
    get_inshorts_articles().to_json(f'inshorts-{today}.json')