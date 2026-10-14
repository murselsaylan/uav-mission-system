from selenium import webdriver
from selenium.webdriver.common.by import By as by
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
# Tarayıcı ayarları
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
options = Options()
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
# Selenium başlat
driver = webdriver.Chrome(options=options)
actions=ActionChains(driver=driver)
driver.implicitly_wait(5)
driver.get("https://www.booking.com/searchresults.tr.html?ss=Dortmund%2C+North+Rhine-Westphalia%2C+Almanya&ssne=Sak%C4%B1z&ssne_untouched=Sak%C4%B1z&efdco=1&label=gen173nr-10CAEoggI46AdIM1gEaOQBiAEBmAEzuAEXyAEM2AED6AEB-AEBiAIBqAIBuAKGqMnEBsACAdICJGRlYmFhODc3LWJlNGYtNDU4Ny1hZWJiLWU4NjQ0Yzc3N2U0YdgCAeACAQ&sid=3fba183582aaedd004f2043acdf41794&aid=304142&lang=tr&sb=1&src_elem=sb&src=index&dest_id=-1761123&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=tr&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=427b857374b804cb&ac_meta=GhA0MjdiODU3Mzc0YjgwNGNiIAAoATICdHI6BmRPUlRNVUAASgBQAA%3D%3D&checkin=2025-08-08&checkout=2025-08-10&ltfd=1%3A1%3A8-2025_9-2025_10-2025%3A1%3A1&group_adults=1&no_rooms=1&group_children=0")
time.sleep(2)

hotels=driver.find_elements(by.XPATH,'//div[@data-testid="property-card-container"]')
print(len(hotels))
for hotel in hotels:
    name=hotel.find_element(by.CSS_SELECTOR,'h3 div[data-testid="title"]').text
    container=hotel.find_element(by.CSS_SELECTOR,'div[data-testid="availability-single"]')
    container=container.find_element(by.CSS_SELECTOR,'div[data-testid="availability-rate-information"]')
    price=int(container.find_element(by.CSS_SELECTOR,'span[data-testid="price-and-discounted-price"]').text.replace('TL','').replace('.','').strip())
    print(price)