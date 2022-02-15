"""
groupfuncs.py

Support functions for groups
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def get_group_link_elements(driver, wait):
    '''
    gets a tags inside the divs for groups
    '''
    try:
        group_div_xpath = '//div[@data-visualcompletion="ignore-dynamic"]/a'
        wait.until(EC.presence_of_element_located((By.XPATH, group_div_xpath)))
        groups = driver.find_elements(By.XPATH, group_div_xpath)
        return groups
    except:
        return None


def scroll_into_view(driver, element):
    '''
    scrolls untils the element is visible on the screen
    '''
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
    except:
        print("[*] => (scroll_into_view) - Error while scrolling to the element")


def leave_group(wait):
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="Joined"]'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="Leave group"]'))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, '//span[text()="Leave Group"]'))).click()
            return True
        except:
            return False


def switch_tab(driver, window_handle):
    try:
        driver.switch_to.window(window_handle)
        return True
    except:
        return False


def open_new_tab(driver):
    '''
    opens a new tab and returns the handle
    '''
    try:
        driver.execute_script("window.open('');")
        return driver.window_handles[len(driver.window_handles)-1]
    except:
        return None


def get_excluded_group_names(fname):
    '''
    reads group names from a file
    '''
    with open(fname,'rb') as fh:
        content = fh.read()
        group_names_split = content.decode('utf-8').split('\n')
        group_names = [name.lower() for name in group_names_split if name != '']
        group_names = list(map(lambda name: name.replace('\r',''), group_names))
        group_names = [name for name in group_names if name != '']
        return group_names


def dump_groups(groups, fname):
    '''
    dumps the group names into a file
    '''
    with open(fname, 'wb') as fh:
        for group in groups:
            group_name = group.text.split('\n')[0]
            if group_name.lower() not in ['your feed', 'discover', 'your notifications']:
                fh.write(group_name.encode('utf-8'))
                fh.write("\n".encode('utf-8'))
  