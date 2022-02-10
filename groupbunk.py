"""
GroupBunk v.1

Leave your Facebook groups quietly 

Author: Shine Jayakumar
Github: https://github.com/shine-jayakumar

LICENSE: MIT
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

import logging
import sys
from datetime import datetime
import time

from groupfuncs import *
import param_funcs as pf

start_time = time.time()

IGNORE_DIV = ['your feed', 'discover', 'your notifications']

FB_GROUP_URL = 'https://www.facebook.com/groups/feed/'


DEFAULT_PARAMS = {
    "EXCLUDE_GROUPS_FNAME": None,
    "ELEMENT_LOAD_TIMEOUT": 30,
    "GROUP_NAME_LOAD_TIME": 4,
    "MAX_RECAPTURE_RETRIES":5,
    "DUMP_GROUPS_FNAME": None,
    "FB_USERNAME": None,
    "FB_PASSWORD": None,
}


if len(sys.argv) < 2 or len(sys.argv) % 2 == 0 or not pf.check_params_present(['-u','-p'], sys.argv):
    pf.display_help()
    sys.exit()

#loading command line arguments
pf.load_params(sys.argv, DEFAULT_PARAMS)


def display_intro():
    intro = """
    GroupBunk v.1
    Leave your Facebook groups quietly

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    
    """
    print(intro)


# Setting up logger
# =====================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(lineno)d:%(levelname)s:%(message)s")
file_handler = logging.FileHandler(
    f'groupbunk_{datetime.now().strftime("%d_%m_%Y__%H_%M_%S")}.log', 'w', 'utf-8')
file_handler.setFormatter(formatter)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
#=======================================================



display_intro()
logger.info("script started")

# loading group names to be excluded
if DEFAULT_PARAMS['EXCLUDE_GROUPS_FNAME']:
    logger.info("Loading group names to be excluded")
    excluded_group_names = get_excluded_group_names(DEFAULT_PARAMS['EXCLUDE_GROUPS_FNAME'])
    IGNORE_DIV.extend(excluded_group_names)


options = Options()
# supresses notifications
options.add_argument("--disable-notifications")

logger.info("Downloading latest chrome webdriver")
# UNCOMMENT TO SPECIFY DRIVER LOCATION
# driver = webdriver.Chrome("D:/chromedriver/98/chromedriver.exe", options=options)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

if not driver:
    logger.critical('Unable to download chrome webdriver for your version of Chrome browser')
    sys.exit()

logger.info("Successfully downloaded chrome webdriver")

wait = WebDriverWait(driver, DEFAULT_PARAMS['ELEMENT_LOAD_TIMEOUT'])

try:
    logger.info(f"Opening FB GROUPS URL: {FB_GROUP_URL}")
    driver.get(FB_GROUP_URL)

    logger.info("Sending username")
    wait.until(EC.visibility_of_element_located((By.ID, 'email'))).send_keys(DEFAULT_PARAMS['FB_USERNAME'])

    logger.info("Sending password")
    driver.find_element(By.ID, 'pass').send_keys(DEFAULT_PARAMS['FB_PASSWORD'])

    logger.info("Clicking on Log In")
    wait.until(EC.presence_of_element_located((By.ID, 'loginbutton'))).click()

    # get all the links inside divs representing group names
    group_links = get_group_link_elements(driver, wait)

    if not group_links:
        logger.error("Unable to find links")
        sys.exit()

    no_of_currently_loaded_links = 0

    logger.info(f"Initial link count: {len(group_links)-3}")
    logger.info("Scrolling down to capture all the links")

    # scroll until no new group links are loaded
    while len(group_links) > no_of_currently_loaded_links:
        no_of_currently_loaded_links = len(group_links)
        print(f"Updated link count: {no_of_currently_loaded_links-3}")
        scroll_into_view(driver, group_links[no_of_currently_loaded_links-1])
        time.sleep(DEFAULT_PARAMS['GROUP_NAME_LOAD_TIME'])
        # re-capturing
        group_links = get_group_link_elements(driver, wait)  

    logger.info(f"Total number of links found: {len(group_links)-3}")
     
    # only show the group names and exit
    if DEFAULT_PARAMS['DUMP_GROUPS_FNAME']:
        logger.info('ONLY SHOW GROUPS parameter set to True')
        logger.info(f"Dumping group names to: {DEFAULT_PARAMS['DUMP_GROUPS_FNAME']}")
        dump_groups(group_links, DEFAULT_PARAMS['DUMP_GROUPS_FNAME'])
        driver.quit()
        sys.exit()
    
    # first 3 links are for Your feed, 'Discover, Your notifications
    i = 0
    save_state = 0
    no_of_retries = 0
    failed_groups = []
    total_groups = len(group_links)

    while i < total_groups:
        try: 
            # need only the group name and not Last Active
            group_name = group_links[i].text.split('\n')[0]

            # if group name not in ignore list
            if group_name.lower() not in IGNORE_DIV:
                logger.info(f"Leaving group: {group_name}")
                link = group_links[i].get_attribute('href')
                logger.info(f"Opening group link: {link}")
                switch_tab(driver, open_new_tab(driver))
                driver.get(link)
                if not leave_group(wait):
                    logger.info('Unable to leave the group. You might not be a member of this group.')
                driver.close()
                switch_tab(driver, driver.window_handles[0])
            else:
                if group_name.lower() not in ['your feed', 'discover', 'your notifications']:
                    logger.info(f"Skipping group : {group_name}")
            i += 1
                
        except StaleElementReferenceException:
            logger.error('Captured group elements gone stale. Recapturing...')
            if no_of_retries > DEFAULT_PARAMS['MAX_RECAPTURE_RETRIES']:
                logger.error('Reached max number of retry attempts')
                break
            save_state = i
            group_links = get_group_link_elements(driver, wait)
            no_of_retries += 1
        except Exception as ex:
            logger.error(f"Unable to leave group {group_name}. Error: {ex}")
            failed_groups.append(group_name)
            i += 1
    total_no_of_groups = len(group_links)-3
    total_no_failed_groups = len(failed_groups)
    logger.info(f"Total groups: {total_no_of_groups}")
    logger.info(f"No. of groups failed to leave: {total_no_failed_groups}")
    logger.info(f"Success percentage: {((total_no_of_groups - total_no_failed_groups)/total_no_of_groups) * 100} %")
    if failed_groups:
        failed_group_names = ", ".join(failed_groups)
        logger.info(f"Failed groups: \n{failed_group_names}")
    

except Exception as ex:
    logger.error(f"Script ended with exception: {ex}")

finally:
    end_time = time.time()
    logger.info(f"Total time taken: {round(end_time - start_time, 4)} seconds")
    if driver:
        driver.quit()
