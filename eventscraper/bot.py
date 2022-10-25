import os

import discord
from discord.ext import tasks
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()


class EventScraper(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.events_channel_id = 1031742574836322327
        self.base_url = "https://ra.co"
        self.url = f"{self.base_url}/events/us/washingtondc" 
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=chrome_options)
        self.newest_video = None
        self.current_urls = set()

        # start the task to run in the background
        self.ra_co_scraper.start()

    @tasks.loop(seconds=60)
    async def ra_co_scraper(self):
        try:
            self.browser.implicitly_wait(10)
            self.browser.get(self.url)
            content = self.browser.page_source.encode("utf-8")
            soup = BeautifulSoup(content, features="html.parser")
            events = soup.find_all("li", {"class": "Column-sc-18hsrnn-0 fBvJUG"})
            links = set()
            for event in events:
                href_content = event.find(href=True)
                link = f"{self.base_url}{href_content['href']}"
                links.add(link)
            channel = self.get_channel(self.events_channel_id)
            if self.current_urls != links:
                self.current_urls = links
                if channel is not None:
                    for link in self.current_urls:
                        await channel.send(link)
        except TimeoutException:
            print("Loading took too much time!")


    @ra_co_scraper.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

    async def on_ready(self):
        print(f"We have logged in as {client.user}")


if __name__ == "__main__":
    client = EventScraper()
    
    client.run(os.environ["EVENT_DISCORD_BOT_TOKEN"])

