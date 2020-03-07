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

    # NASA Mars News 
    # Get title and paragraph for latest article 
    request_soup(urls.news)
    title_results = soup.find('div', class_="content_title").a.text.strip()
    p_results = soup.find('div', class_="rollover_description_inner").text.strip()

    # JPL Mars Space Images - Featured Image
    # Get the latest featured image title and image url
    # Initialize browser to navigate to page with hires image
    browser = init_browser()
    browser.visit(urls.image)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars_data["headline"] = soup.find("a", class_="result-title").get_text()
    mars_data["price"] = soup.find("span", class_="result-price").get_text()
    mars_data["hood"] = soup.find("span", class_="result-hood").get_text()

    return mars_data
