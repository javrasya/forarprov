import os
import random
import re
import signal
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True


places = [place.strip() for place in os.environ["PLACES"].split(",")]
found_items = {}

ssn = os.environ["SSN"]
starting_time = datetime.strptime(os.environ["START"], "%Y-%m-%d")
ending_time = datetime.strptime(os.environ["END"], "%Y-%m-%d")

if __name__ == '__main__':

    options = Options()
    options.add_argument("user-agent=User-Agent: my-agent")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox ')
    options.headless = True
    driver = webdriver.Chrome(options=options)


    def wait_and_get(search_type, value, multiple=False):
        if multiple:
            return WebDriverWait(driver, 60).until(ec.visibility_of_any_elements_located((search_type, value)))
        else:
            return WebDriverWait(driver, 60).until(ec.visibility_of_element_located((search_type, value)))


    already_searched_before = False
    not_found_text = 'Hittar inga lediga tider som matchar dina val.'


    def search_earliest(place, first_time=False):
        wait_and_get(By.XPATH, "//button[@data-bind='click:selectLocation']").click()
        wait_and_get(By.XPATH, f"//a[normalize-space(@title)='{place}']").click()
        if first_time:
            wait_and_get(By.XPATH, "//button[@data-bind='click:selectVehicleType']").click()
            wait_and_get(By.XPATH, "//a[@title='Ja, automat']").click()
            wait_and_get(By.XPATH, "//button[@data-bind='click:selectVehicleType']").click()
            wait_and_get(By.XPATH, "//a[@title='Ja, automat']").click()
        first_result = wait_and_get(By.XPATH,
                                    f"//div[(@data-bind='foreach:occasions' and contains(.,'{place}')) or contains(.//p[not(contains(@style,'display: none'))],'{not_found_text}')]",
                                    multiple=True)[0]
        text = first_result.text
        if text != not_found_text:
            earliest_date_match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', text, re.MULTILINE)
            if earliest_date_match:
                earliest_date = earliest_date_match.group(1)
                return datetime.strptime(earliest_date, '%Y-%m-%d %H:%M')


    driver.set_window_size(50, 800)
    driver.get("https://fp.trafikverket.se/boka/#/licence")

    wait_and_get(By.ID, 'social-security-number-input').send_keys(ssn)
    wait_and_get(By.XPATH, "//a[@title='B']").click()
    wait_and_get(By.CLASS_NAME, "alreadyBookedExamination").click()
    killer = GracefulKiller()
    while not killer.kill_now:
        for i, place in enumerate(places):
            earliest = search_earliest(place, i == 0)
            valid_earliest = earliest if earliest and starting_time <= earliest <= ending_time else None
            previously_found_date = found_items.get(place, None)

            if not valid_earliest and previously_found_date:
                print(f"Previously found date: {previously_found_date} in {place} is no longer available")

            elif valid_earliest:
                found_items[place] = valid_earliest
                if previously_found_date and valid_earliest > previously_found_date:
                    print(f"Previously found date: {previously_found_date} in {place} is no longer available")
                if valid_earliest != previously_found_date:
                    print(f"Found new slot in {place}: {valid_earliest}, {(valid_earliest - datetime.now()).days} days from now")
        wait_before_next = random.randint(60 * 5, 60 * 20)
        print(f"Search is complete, will start another in {wait_before_next} seconds")
        sleep(wait_before_next)
    driver.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
