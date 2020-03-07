#Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import pymongo

urls = {
        'news': 'https://mars.nasa.gov/news/',
        'image': 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars',
        'weather': 'https://twitter.com/marswxreport?lang=en',
        'facts' : 'https://space-facts.com/mars/',
        'hemi' : 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
}

def request_soup(url):
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    # Initialize mars_data dictionary to hold all scraped values to be entered into mongo db
    mars_data = {}



    #############################################################
    # NASA Mars News - Scrape section                           #
    # Get title and paragraph for latest article                #
    request_soup(urls.news)
    news_title = soup.find('div', class_="content_title").a.text.strip()
    news_paragraph = soup.find('div', class_="rollover_description_inner").text.strip()



    #############################################################
    # JPL Mars Space Images Featured Image - Scrape section     #
    # Get the latest featured image title and image url         #
    # Initialize browser and navigate to page with hires image  #
    browser = init_browser()
    browser.visit(urls.image)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    # Now that we are on the right page create Beautiful soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # parse soup object 
    feat_img = soup.find('figure', class_='lede')

    # modify relative url from src to absolute url 
    featured_image_url = f'https://www.jpl.nasa.gov{feat_img.a.img["src"]}'



    #############################################################
    # Mars Weather - Scrape section                             #
    # Get weather tweets information from twitter                #
    request_soup(urls.weather)
    tweets = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    # Loop through returned results and match the first tweet that starts with 'Insight sol'
    for tweet in tweets:
    # Error handling if there is something wrong with the tweet
    try:
        # Create a regular expression to match the first phrase of a tweet about the weather
        regex = '^InSight sol'
        # Test is the tweet starts with the regex expression
        if re.match(regex,tweet.text) is not None:
            # capture the tweet and exit the for loop
            weather_data = tweet.text
            break
    except AttributeError as e:
        print(e)



    #############################################################
    # Mars Facts - Scrape section                               #
    # Use pandas to read the html table data on the page into a list of dictionaries
    tables = pd.read_html(url)

    # Read the first dictionary in the list into a pandas dataframe and name columns
    df = tables[0]
    df.columns = ['Parameter', 'Value']

    # Set the Parameter column to the index
    df.set_index('Parameter', inplace=True)

    # Convert the dataframe into an html table, strip the end of line newlines and 
    # write the result to an html file to view 
    fact_table = df.to_html()
    fact_table = fact_table.replace('\n', '')
 


    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars_data["headline"] = soup.find("a", class_="result-title").get_text()
    mars_data["price"] = soup.find("span", class_="result-price").get_text()
    mars_data["hood"] = soup.find("span", class_="result-hood").get_text()

    return mars_data
