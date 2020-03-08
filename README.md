# Web Scraping  - Mission to Mars

![mission_to_mars](Missions_to_Mars/Images/mission_to_mars.png)

A web application was built that scrapes various Mars related websites for data related to the Mission to Mars and displays the information in a single HTML page. The code to do the scraping is captured in a [Jupyter Notebook](Missions_to_Mars/mission_to_mars.ipynb). This code was revised and put into a python .py file named [scrape_mars.py](Missions_to_Mars/scrape_mars.py) in a function to be called upon by a flask [app.py](Missions_to_Mars/app.py) when a button is clicked on the website calling the /scrape path.


##  Scraping Mars data

Initial scraping was completed using [Jupyter Notebook](Missions_to_Mars/mission_to_mars.ipynb) using BeautifulSoup, Pandas, and Requests/Splinter. The locations and types of data that were scraped follows.


### NASA Mars News

* The [NASA Mars News Site](https://mars.nasa.gov/news/)  latest News Title and Paragraph Text was scraped. The data was assigned to the following variables for reference later:

`news_title`

`news_paragraph` 

### JPL Mars Space Images - Featured Image

The JPL Featured Space Image was scraped from: [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars) and stored in the following variable:

`featured_image_url`


### Mars Weather

The Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) was scraped for the latest Mars weather tweet from the page. Tweets which were not weather tweets were filtered out in order to get the latest weather tweet. The result was stored in the following variable:

`weather_data`


### Mars Facts

The Mars Facts webpage [here](https://space-facts.com/mars/) was used along with Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc. The information was stored in the following variable:

`fact_table`

### Mars Hemispheres

The USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) was used to obtain four high resolution images for each of Mar's hemispheres. The urls and titles were stored in a variable as a dictionary similar to the example below:

```python
# Example:
hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    {"title": "Cerberus Hemisphere", "img_url": "..."},
    {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    {"title": "Syrtis Major Hemisphere", "img_url": "..."},
]
```

- - -

##  MongoDB and Flask Application

MongoDB with Flask templating was used to create a new HTML page that displays all of the information that was scraped from the URLs above.

* The Jupyter notebook was transformed into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of the scraping code from above and return one Python dictionary containing all of the scraped data.

* A route called `/scrape` was created that will import your `scrape_mars.py` script and call your `scrape` function.

  * The return value was stored in Mongo as a Python dictionary.

* A root route `/` was created that will query ther Mongo database and pass the mars data into an HTML template to display the data.

* A template HTML file called `index.html` was created that takes the mars data dictionary and displays all of the data in the appropriate HTML elements. 

The results that are rendered after clicking the "Scrape New Data" button is below:

![screencapture.png](Missions_to_Mars/Images/screencapture.png)
