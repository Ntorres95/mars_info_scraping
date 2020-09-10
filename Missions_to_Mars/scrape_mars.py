# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

#url where we're pulling the info from
nasa_url = "https://mars.nasa.gov/news/"
jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
facts_url = "https://space-facts.com/mars/"
hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

#requests from the nasa url
nasa_response = requests.get(nasa_url)

#bs of the nasa_response
nasa_soup = BeautifulSoup(nasa_response.text, 'html.parser')

#get the title and content of the latest article
news_title = nasa_soup.find('div', class_="content_title").a.text
news_p = nasa_soup.find('div', class_="rollover_description_inner").text

#sanity check
#print(news_title)
#print(news_p)

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

#using splinter to navigate to jpl images site
browser.visit(jpl_url)

#click the Full Image link
browser.click_link_by_partial_text('FULL IMAGE')

#click the more info link
browser.click_link_by_partial_text('more info')

#click the image to get the full size image url
browser.click_link_by_partial_href('/spaceimages/images')

#save the url of the full size image
featured_image_url = browser.url

#close the browser
browser.quit()

#sanity check
#print(featured_image_url)

#scrape the facts about mars
#request for the facts url
facts_response = requests.get(facts_url)

#bs of the facts response
fact_soup = BeautifulSoup(facts_response.text, 'html')

#sanity check
#print(fact_soup)

#get onl the column 2's
columns = fact_soup.find_all('td', class_='column-2')

#sanity check
#print(columns[1].text)

#save the equatorial diameter
equa_d = columns[0].text

#save the  diameter
polar_d = columns[1].text

#save the mass
mass = columns[2].text

#save the moons
moons = columns[3].text

#save the orbit distance
orb_d = columns[4].text

#save the orbit period
orb_p = columns[5].text

#save the surface temp
surf_t = columns[6].text

#save the first record
first_rec = columns[7].text

#save the recorded by
rec_by = columns[8].text

#sanity check
#print(rec_by)

facts_dict = {"Equatorial Diameter":[equa_d],
             "Polar Diameter":[polar_d],
             "Mass":[mass],
             "Moons":[moons],
             "Orbital Diameter":[orb_d],
             "Orbital Period":[orb_p],
             "Surface Temperature":[surf_t],
             "First Record":[first_rec],
             "Recorded By":[rec_by]}

#create a facts df to be converted
facts_df = pd.DataFrame(facts_dict)

#sanity check
#print(facts_df.head)

#convert to html
html_table = facts_df.to_html

#sanity check
#print(html_table)

#list for the hemisphere image urls
hemisphere_image_urls = []

#dict for the 

#list of hemisphere image names
names = ["Valles Marineris Hemisphere Enhanced",
         "Cerberus Hemisphere Enhanced",
         "Schiaparelli Hemisphere Enhanced",
        "Syrtis Major Hemisphere Enhanced"]

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

#using splinter to navigate to hemispheres site
browser.visit(hemi_url)

#loop to cycle through all the pages
for name in names:

    #click the image links
    browser.click_link_by_partial_text(name)

    #click the Sample button to get the full size image url
    browser.click_link_by_text('Sample')

    #save the browser url
    img_url = browser.url
    
    #sanity check
    #print(img_url)
    
    #append the list
    hemisphere_image_urls.append({"title": name, "img_url": img_url})
    
    #return to the original url
    browser.visit(hemi_url)
    
#close the browser
browser.quit()

#sanity check
#print(hemisphere_image_urls)