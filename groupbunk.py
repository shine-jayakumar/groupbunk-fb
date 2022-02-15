"""
GroupBunk v.1.2

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
import argparse
import logging
import sys
from datetime import datetime
import time
from groupfuncs import *
import os

# suppress webdriver manager logs
os.environ['WDM_LOG_LEVEL'] = '0'

IGNORE_DIV = ['your feed', 'discover', 'your notifications']
FB_GROUP_URL = 'https://www.facebook.com/groups/feed/'


def display_intro():
    '''
    Displays intro of the script
    '''
    intro = """
    GroupBunk v.1.2
    Leave your Facebook groups quietly

    Author: Shine Jayakumar
    Github: https://github.com/shine-jayakumar
    
    """
    print(intro)


def time_taken(start_time, logger):
    '''
    Calculates the time difference from now and start time
    '''
    end_time = time.time()
    logger.info(f"Total time taken: {round(end_time - start_time, 4)} seconds")


def cleanup_and_quit(driver):
    '''
    Quits driver and exits the script
    '''
    if driver:
        driver.quit()
    sys.exit()


start_time = time.time()

# ====================================================
# Argument parsing
# ====================================================
description = "Leave your Facebook groups quietly"
usage = "groupbunk.py username password [-h] [-eg FILE] [-et TIMEOUT] [-sw WAIT] [-gr RETRYCOUNT] [-dg FILE]"
examples="""
Examples:
groupbunk.py bob101@email.com bobspassword101
groupbunk.py bob101@email.com bobspassword101 -eg keepgroups.txt
groupbunk.py bob101@email.com bobspassword101 -et 60 --scrollwait 10 -gr 7
groupbunk.py bob101@email.com bobspassword101 --dumpgroups mygroup.txt --groupretry 5
"""
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description,
    usage=usage,
    epilog=examples,
    prog='groupbunk')

# required arguments
parser.add_argument('username', type=str, help='Facebook username')
parser.add_argument('password', type=str, help='Facebook password')

# optional arguments
parser.add_argument('-eg', '--exgroup',    type=str, metavar='', help='file with group names to exclude (one group per line)')
parser.add_argument('-et', '--eltimeout',  type=int, metavar='', help='max timeout for elements to be loaded', default=30)
parser.add_argument('-sw', '--scrollwait', type=int, metavar='', help='time to wait after each scroll', default=4)
parser.add_argument('-gr', '--groupretry', type=int, metavar='', help='retry count while recapturing group names', default=5)
parser.add_argument('-dg', '--dumpgroups', type=str, metavar='', help='do not leave groups; only dump group names to a file')
parser.add_argument('-v', '--version', action='version', version='%(prog)s v.1.2')
args = parser.parse_args()
# ====================================================


# Setting up logger
# =====================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(lineno)d:%(levelname)s:%(message)s")
file_handler = logging.FileHandler(f'groupbunk_{datetime.now().strftime("%d_%m_%Y__%H_%M_%S")}.log', 'w', 'utf-8')
file_handler.setFormatter(formatter)

stdout_formatter = logging.Formatter("[*] => %(message)s")
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(stdout_formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
#=======================================================


try:

    display_intro()
    logger.info("script started")

    # loading group names to be excluded
    if args.exgroup:
        logger.info("Loading group names to be excluded")
        excluded_group_names = get_excluded_group_names(args.exgroup)
        IGNORE_DIV.extend(excluded_group_names)

    options = Options()
    # supresses notifications
    options.add_argument("--disable-notifications")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--log-level=3")

    logger.info("Downloading latest chrome webdriver")
    # UNCOMMENT TO SPECIFY DRIVER LOCATION
    # driver = webdriver.Chrome("D:/chromedriver/98/chromedriver.exe", options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    if not driver:
        raise Exception('Unable to download chrome webdriver for your version of Chrome browser')

    logger.info("Successfully downloaded chrome webdriver")

    wait = WebDriverWait(driver, args.eltimeout)

    logger.info(f"Opening FB GROUPS URL: {FB_GROUP_URL}")
    driver.get(FB_GROUP_URL)

    logger.info("Sending username")
    wait.until(EC.visibility_of_element_located((By.ID, 'email'))).send_keys(args.username)

    logger.info("Sending password")
    driver.find_element(By.ID, 'pass').send_keys(args.password)

    logger.info("Clicking on Log In")
    wait.until(EC.presence_of_element_located((By.ID, 'loginbutton'))).click()

    # get all the links inside divs representing group names
    group_links = get_group_link_elements(driver, wait)

    if not group_links:
        raise Exception("Unable to find links")

    no_of_currently_loaded_links = 0

    logger.info(f"Initial link count: {len(group_links)-3}")
    logger.info("Scrolling down to capture all the links")

    # scroll until no new group links are loaded
    while len(group_links) > no_of_currently_loaded_links:
        no_of_currently_loaded_links = len(group_links)
        logger.info(f"Updated link count: {no_of_currently_loaded_links-3}")
        scroll_into_view(driver, group_links[no_of_currently_loaded_links-1])
        time.sleep(args.scrollwait)
        # re-capturing
        group_links = get_group_link_elements(driver, wait)  

    logger.info(f"Total number of links found: {len(group_links)-3}")
     
    # only show the group names and exit
    if args.dumpgroups:
        logger.info('Only dumping group names to file. Not leaving groups')
        logger.info(f"Dumping group names to: {args.dumpgroups}")
        dump_groups(group_links, args.dumpgroups)
        time_taken(start_time, logger)
        cleanup_and_quit(driver)
    
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
            if no_of_retries > args.groupretry:
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
    time_taken(start_time, logger)
    cleanup_and_quit(driver)