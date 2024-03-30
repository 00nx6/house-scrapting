from bs4 import BeautifulSoup as bs
import requests
import postgresqlite
import re
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# grab site url
# construct filters needed
# go to site url, scrape card format (a-tag) results from filtered houses.
# save a-tag link somewhere
# nav to div child with 'MuiCardContent-root ListingCard_cardContent__XXXXX' as class tags
# save inner text from 'ListingCard_listingRow__npJi4' for location and size
# for availability date: 'MuiTypography-root MuiTypography-body2 mui-style-1fsfdy1'
# check saved results against program filters, eliminate what isnt good (e.g too small or available too early or too late)
# go though saved urls and scrape for further info
# and the rest is for later to figure out : )

def load_file(file_name: str):
    with open(file_name) as file:
        keys = file.readline().strip().split(';')
        sites = []
        for line in file:
            _dict = {}
            for key, data in zip(keys, line.strip().split(';')):
                _dict[key] = data
            sites.append(_dict)
    return sites


def open_site(site_info):
    # for site navigation onlyexpat and smart wonen are not finished, most other ones work 9/10 times.
    options = Options()
    options.set_preference('webdriver.firefox.driver', './geckodriver')
    driver = webdriver.Firefox(options=options)
    print(site_info)
    driver.get(site_info['url'])
    time.sleep(2)
    
    # try to find a search bar
    try:
        search_bar = driver.find_element(By.ID, site_info['search_bar'])
    except Exception:
        search_bar = driver.find_element(By.CLASS_NAME, site_info['search_bar'])

    if site_info['name'].lower() == 'domica':
        driver.execute_script("document.getElementById('usercentrics-root').style.display = 'none';")
        new_search_bar = driver.find_element(By.CLASS_NAME, 'ss-search').find_element(By.XPATH, './/input')
        new_search_bar.send_keys('Enschede')
        time.sleep(.2)
        new_search_bar.send_keys(Keys.DOWN, Keys.ENTER)
        submit = driver.find_element(By.ID, 'eazlee_filter_field_button_search')
        submit.click()
        
    search_bar.send_keys('Enschede')
    time.sleep(2)
    
    if site_info['name'] == 'Erasmus play':
        driver.find_element(By.ID, 'search-results').click()
    else:
        search_bar.send_keys(Keys.ENTER)
    
    if site_info['name'].lower() == 'Student union kamersite'.lower():
        driver.find_element(By.XPATH, "//*[contains(@class, 'ctabutton ') and contains(@class, 'tc-orange-darkhover')]").click()
        
    time.sleep(2)
    driver.close()
        

def main():
    sites = load_file('sites.csv')
    for site in sites:
        open_site(site)



if __name__ == "__main__":
    main()