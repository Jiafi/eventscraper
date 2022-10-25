from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

chrome_options = Options()
# chrome_options.add_argument("--headless")

url = "https://ra.co/events/us/washingtondc"
browser = webdriver.Chrome(options=chrome_options)
delay = 120 # seconds
try:
    # myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'Column-sc-18hsrnn-0 fBvJUG')))
    # print("Page is ready!")
    browser.implicitly_wait(10)
    browser.get(url)
    content = browser.page_source.encode("utf-8")
    soup = BeautifulSoup(content, features="html.parser")
    events = soup.find_all("li", {"class": "Column-sc-18hsrnn-0 fBvJUG"})
    links = set()
    for event in events:
        href_content = event.find(href=True)
        link = f"https://ra.co{href_content['href']}"
        links.add(link)
    print(links)
except TimeoutException:
    print("Loading took too much time!")


