import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which 

class CoinSpiderSelenium(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = [
        'https://web.archive.org/web/20200116052415/https://www.livecoin.net/en'
    ]

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_path = which("chromedriver")


        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver.get("https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/")
        driver.set_window_size(1920, 1080)

        rur_tab = driver.find_element_by_class_name("filterPanelItem___2z5Gb")
        rur_tab[4].click()

        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        for currency in resp.xpath("//div[contains(@class,'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield {
                'currency pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume(24H)': currency.xpath(".//div[2]/span/text()").get()
            }
