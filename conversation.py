import csv
import hashlib
import os
from time import sleep
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# add constant data directory path for saving conversation data
DATA_DIR = 'data'

def collect_conversation_solved_elements_from_tidio(config, driver):
    wait = WebDriverWait(driver, 10)
    driver.get('https://www.tidio.com/panel/inbox/conversations/solved/')
    sleep(10)

    # scrolling to the bottom of the page div[data-palette] div.css-or3pbt + ul.css-1fabh1u    
    # driver.execute_script('document.querySelector("div[data-palette] div.css-or3pbt + ul.css-1fabh1u").scroll(0, 100000);')
    
    is_scroll = True
    while is_scroll:
        conversation_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-palette] ul li')))
        sleep(10)
        # Get the conversation IDs
        old_len = len(conversation_elements)
        # scrolling to the bottom of the page div[data-palette] div.css-or3pbt + ul.css-1fabh1u
        driver.execute_script('document.querySelector("div[data-palette] div.css-or3pbt + ul.css-1fabh1u").scroll(0, 100000);')
        sleep(10)
        conversation_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-palette] ul li')))
        new_len = len(conversation_elements)
        if old_len == new_len:
            is_scroll = False

    return conversation_elements

def get_conversation_hrefs(conversation_elements):
    conversation_hrefs = []
    for conversation_element in conversation_elements:        
        conversation_href = conversation_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        conversation_hrefs.append(conversation_href)
    return conversation_hrefs

def get_conversation_id(conversation_href):
    return conversation_href.split('/')[-1]

def download_conversations_data_from_tidio(config, conversation_hrefs):
    for conversation_href in conversation_hrefs:
        conversation_id_key = get_conversation_id(conversation_href)
        download_url = make_download_url_from_conversation_id(config, conversation_id_key)
        download_conversation_data_from_tidio(download_url)
        
def make_download_url_from_conversation_id(config, conversation_id_key):
    download_url_str = 'https://api-v2.tidio.com/conversations/export?api_token='
    download_url_str += config.get_tidio_api_token()
    download_url_str += '&project_public_key='
    download_url_str += config.get_tidio_api_key()
    download_url_str += '&visitor_id='
    download_url_str += conversation_id_key
    download_url_str += '&time_zone='
    download_url_str += config.get_tidio_time_zone()
    download_url = f'{download_url_str}'
    return download_url

def download_conversation_data_from_tidio(download_url):    
    prepare_data_dir()
    # make hash from url
    download_url_hash = hashlib.md5(download_url.encode()).hexdigest()
    downloaded_filename = f'conversation_data_{download_url_hash}.csv'
    # download conversation data as csv file
    response = requests.get(download_url)
    file_path = DATA_DIR + '/' + downloaded_filename
    # save conversation data to csv file
    with open(file_path, 'wb') as f:
        f.write(response.content)

def prepare_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, 0o777)

def data_dir_has_conversation_data_files():
    return len(get_all_conversation_data_files_names()) > 0

def data_dir_has_merged_conversation_data_file():
    return 'merged_conversations_data.csv' in get_all_conversation_data_files_names()

def merge_conversations_data_from_tidio():
    files_names = get_all_conversation_data_files_names()

    merdges_result = []
    for file_name in files_names:
        with open (DATA_DIR + '/' + file_name, 'r') as f:
            conversation_id = file_name.split('_')[-1].split('.')[0]
            reader = csv.reader(f)
            # get header
            header = next(reader)
            for row in reader:
                # convert row to associative array
                row_dict = dict(zip(header, row))
                row_dict['conversation_id'] = conversation_id
                merdges_result.append(row_dict)

    return merdges_result

def prepare_dict_to_csv(data):
    header = data[0].keys()
    rows = [header]
    for row in data:
        rows.append([row[key] for key in header])
    return rows

def save_merged_conversations_data_to_csv(merged_conversations_data):
    with open(DATA_DIR + '/merged_conversations_data.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(merged_conversations_data)

def get_all_conversation_data_files_names():
    files_names = os.listdir(DATA_DIR)
    return files_names
