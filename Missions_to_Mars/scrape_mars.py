#Import Splinter, Beautiful Soup and Pandas

from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    #initiate headless driver for deployment. Headless arguement = True runs in the background, will not open empty browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_p = mars_news(browser)
    
    #run all scaping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image(browser),
        "facts": mars_fact(),
        "hemisphere": hemisphere_image_urls(browser),
        "last_modified": dt.datetime.now()
    }
    
    #Stop web driver and return data
    browser.quit()
    return data

def mars_news(browser):
    # scrape Mars News
    # visit the Mars Nasa news site
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    #convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # add try/except for error handling
    #try:
    slide_elem = news_soup.select_one('ul.item_list li.slide')
        # use the parent element to find the first 'a' tag and save as 'news_title'
    news_title = slide_elem.find("div", class_='content_title').get_text()
        # use the parent element fo find the paragraph text
    news_paragraph = slide_elem.find("div", class_="article_teaser_body").get_text()
        
    #except AttributeError:
        #return None, None
    return news_title, news_paragraph
    
def featured_image(browser):
        # visit url
    url ='https://spaceimages-mars.com'
    browser.visit(url)
        
        # find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
        
        # parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
        
        #add try/except for error handling
        #try: 
            # find the relative image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
            
        # except AttributeError"
        #    return None
        
        #use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
        
    return img_url
    
def mars_fact():
        # add try/except for error handling
        #try:
        # use 'read_html' to scrape the facts table into a dataframe
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
            
        # except BaseException
        #  return None
        
        #assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
        
        #convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")
    
def hemisphere_image_urls(browser):
    #url = 'https://marshemispheres.com/'
        
    #browser.visit(url + 'índex.html')

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)   
    #create a list to hold the images and titles
    hemisphere_image_urls = []

#get a list of all of the hemispheres (find anchor tag with a class of product-item, get child tag of image)
    links = browser.find_by_css('a.product-item img')

#loop through the links, click the link, find the sample anchor, return the href
    for i in range (len(links)):
        hemisphere = {}

    #find the element on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
    
    #find the sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text ('Sample').first
        hemisphere['img_url'] = sample_elem ['href']
    
    #get hemisphere title
        hemisphere['title'] = browser.find_by_css('h2.title').text
    
    #append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
    
    #splinter will navigate back
        browser.back()
        
    return hemisphere_image_urls
    
def scrape_hemisphere(html_text):
        #parse html text
    hemi_soup = soup(html_text, "html.parser")
        
        #adding try/except for error handling
    try: 
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")
                                     
    except AttributeError:
        #Image error will return None, for better front-end handling
        title_elem = None
        sample_elem = None
                                     
    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
        }
        
    return hemispheres
                                     
if __name__ == "__main__":
                                     
    #if running as script, print scraped data
    print(scrape())
                           
                               