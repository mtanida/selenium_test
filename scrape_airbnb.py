import time
import random
from selenium import webdriver

config = None

def min_pause():
    time.sleep(config.MIN_PAUSE_SEC)

def short_pause():
    time.sleep(config.SHORT_PAUSE_SEC)

def long_pause():
    time.sleep(config.LONG_PAUSE_SEC)

def random_pause():
    pause_ms = random.sample(config.RANDOM_PAUSE_SEC, 1)
    time.sleep(pause_ms[0])

def run(local_config):

    # Make config global scope so we don't need to pass it around to
    # every function
    global config
    config = local_config

    # Start the chrome webdriver
    try:
        browser = webdriver.Chrome(config.CHROMEDRIVER_PATH)
        long_pause()
    except webdriver.WebDriverException as e:
        print('The following error occurred starting chromedriver:')
        print(e)
        return

    # Go to airbnb website
    browser.get('https://www.airbnb.com')
    long_pause()

    # top level search 
    main_search(browser)

def main_search(browser):
    for search_term in config.SEARCH_TERMS:
        do_search(browser, search_term)

def do_search(browser, search_term):

    # Click the search box 
    button = browser.find_element_by_xpath('//*[@id="site-content"]/div[1]/div/div/div/div[2]/div/div/div/div/button')
    button.click()

    min_pause()

    # Enter search term
    search_box = browser.find_element_by_css_selector('#GeocompleteController-via-SearchBar')
    search_box.send_keys(search_term + '\n')

    short_pause()

    # Press "Home" button because we're not interested in "Experiences"
    try:
        button = browser.find_element_by_xpath('//*[@id="site-content"]/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/button')
        if button:
            button.click()
    except:
        pass

    short_pause()

    # Iterate over all of the search results
    process_search_results(browser)

def process_search_results(browser):

    # Save main window handle
    main_window_handle = browser.window_handles[0]

    # Current page is 1
    page = 1

    # Loop over all listings for this search result
    while (True):

        # Get element containing the listings
        elem = browser.find_element_by_xpath('//*[@id="site-content"]/div/div[2]/div/div/div/div[2]/div[*]/div/div/div[2]/div/div/div')

        # Get the listing elements on this page
        listings = elem.find_elements_by_xpath('*')

        # Iterate over each listing
        for listing in listings:
            listing.click()

            long_pause()

            browser.switch_to.window(browser.window_handles[-1])

            # Close the tab  
            browser.close()

            # Switch back to main window
            browser.switch_to.window(main_window_handle)

        # Find button to go to next page
        page += 1
        next_page = browser.find_element_by_css_selector('[aria-label="Page ' + str(page) + '"]')  

        # If next page is available, go to it. Else, exit loop
        if next_page:
            next_page.click()
            time.sleep(5)
        else:
            break
        
