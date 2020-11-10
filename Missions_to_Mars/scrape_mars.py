from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Visit NASA Mars Site
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    # HTML object
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    # Return the latest news title and content
    news_title = soup.find('div', class_='bottom_gradient').text
    news_p = soup.find('div', class_='article_teaser_body').text
    #-----------------------------------------------------------------------------------
    # Visit Jet Propulsion Lab
    url = 'https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA14317'
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    # Return the featured Mars image 

    image = soup.find('figure', class_='lede')
    link = image.a['href']

    f_link = 'https://www.jpl.nasa.gov/'+link

    #-----------------------------------------------------------------------------------
    # Mars Facts Table
    import pandas as pd 

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_df = tables[0]
    mars_df.set_index(0)
    mars_df.rename(columns = { 1 : 'Mars'}, inplace = True)
    mars_df.index.name = 'Description'
    mars_table = mars_df.to_html('fact_table.html')

    #-----------------------------------------------------------------------------------
    # Mars Hemisphere
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    dict = {}
    resources = soup.find_all('div', class_='item')

    # loop through to find all resouces
    for resource in resources:
        # find hemisphere title
        hemisphere = resource.find('div', class_='description')
        hemisphere_title = hemisphere.find('h3').text
    
    
        # find link to full hemisphere image
        # Click on to full image page
        click = resource.find('a')
        link = click['href']
        hem_url = 'https://astrogeology.usgs.gov'+link
    
        # Use hem_url to get to full image
        browser.visit(hem_url)
        html = browser.html
        soup = bs(html, 'html.parser')
    
        hem_full = soup.find_all('img', class_='wide-image')
        image_full = hem_full[0]['src']
        img_full = 'https://astrogeology.usgs.gov'+image_full

        # Update dictionary with new information
        dict.update({hemisphere_title:img_full})

    # Put all of scraped information into dictionary
    mars_data = {
        'title': news_title,
        'paragraph': news_p,
        'image': f_link,
        'table': mars_table,
        'hem_image': dict
    }


    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data


