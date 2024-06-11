from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import re

class CoinMarketCapScraper:
    def __init__(self, url, browser='firefox', headless=True):
        self.url = url
        self.driver = self.setup_driver(browser, headless)
        self.driver.get(self.url)
    
    def setup_driver(self, browser, headless):
        """Set up the browser driver."""
        if browser.lower() == 'chrome':
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless")
            service = ChromeService('../chromedriver')  # Replace with the path to your chromedriver executable
            driver = webdriver.Chrome(service=service, options=options)
        elif browser.lower() == 'firefox':
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            service = FirefoxService('../geckodriver')  # Replace with the path to your geckodriver executable
            driver = webdriver.Firefox(service=service, options=options)
        else:
            raise ValueError("Unsupported browser: {}".format(browser))
        
        return driver

    def fetch_price_change(self):
        element = self.driver.find_element(By.XPATH, '//*[@id="section-coin-overview"]/div[2]/div/div/p')
        return self.extract_change_with_color(element)

    def fetch_market_cap_change(self):
        element = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[1]/div[1]/dd/div/p')
        return self.extract_change_with_color(element)

    def fetch_volume_change(self):
        element = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[2]/div[1]/dd/div/p')
        return self.extract_change_with_color(element)

    def extract_change_with_color(self, element):
        """Extract numerical change and make it negative if the red component is dominant."""
        text = element.text.strip()
        color = element.value_of_css_property('color')
        number = self.extract_number(text)
        
        # Extract the RGB values from the color string
        rgb = re.findall(r'\d+', color)
        if len(rgb) == 3:
            red, green, blue = map(int, rgb)
            if red > green and red > blue:
                return f"-{number}"
        
        return number

    def fetch_price(self):
        element = self.driver.find_element(By.XPATH, '//*[@id="section-coin-overview"]/div[2]/span')
        return self.extract_number(element.text.strip())


    def fetch_market_cap(self):
        element = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[1]/div[1]/dd')
        return self.extract_number(element.text.strip().split('\n')[1])

    def fetch_market_cap_rank(self):
        element = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[1]/div[2]/div/span')
        return self.extract_number(element.text.strip())

    def fetch_volume(self):
        element = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[2]/div[1]/dd')
        return self.extract_number(element.text.strip().split('\n')[1])

    def fetch_volume_rank(self):
        element = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[2]/div[2]/div/span')
        return self.extract_number(element.text.strip())

    def fetch_circulating_supply(self):
        element = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[4]/div[1]/dd')
        return self.extract_number(element.text.strip())

    def fetch_total_supply(self):
        element = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[5]/div/dd')
        return self.extract_number(element.text.strip())

    def fetch_diluted_market_cap(self):
        element = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[7]/div/dd')
        return self.extract_number(element.text.strip())

    def fetch_official_links(self):
        """Fetch the official links."""
        official_links = []

        # Locate the section containing official links
        official_links_section = self.driver.find_element(By.CSS_SELECTOR, 'div.coin-info-links')

        # Find the second stats-block element containing official links
        official_links_block = official_links_section.find_elements(By.CSS_SELECTOR, 'div[data-role="stats-block"]')[1]

        # Find all link elements within the official links block
        link_elements = official_links_block.find_elements(By.TAG_NAME, 'a')
        
        # Iterate over each link element to extract the name and href
        for link_element in link_elements:
            name = link_element.text.strip()
            link = link_element.get_attribute('href')
            official_links.append({"name": name.lower(), "link": link})
        
        return official_links

    def fetch_social_links(self):
        """Fetch the social links."""
        social_links = []

        # Locate the section containing social links
        social_links_section = self.driver.find_element(By.CSS_SELECTOR, 'div.coin-info-links')

        # Find the third stats-block element containing social links
        social_links_block = social_links_section.find_elements(By.CSS_SELECTOR, 'div[data-role="stats-block"]')[2]

        # Find all link elements within the social links block
        link_elements = social_links_block.find_elements(By.TAG_NAME, 'a')
        
        # Iterate over each link element to extract the name and href
        for link_element in link_elements:
            name = link_element.text.strip()
            url = link_element.get_attribute('href')
            social_links.append({"name": name.lower(), "url": url})
        
        return social_links

    def fetch_contracts(self):
        """Fetch the contract information."""
        contracts = []

        # Locate the section containing contract information
        contracts_section = self.driver.find_element(By.CSS_SELECTOR, 'div.coin-info-links')

        # Find the second stats-block element containing contracts
        contracts_block = contracts_section.find_elements(By.CSS_SELECTOR, 'div[data-role="stats-block"]')[0]

        # Find all contract elements within the contracts block
        contract_elements = contracts_block.find_elements(By.CLASS_NAME, 'chain-name')
        
        # Iterate over each contract element to extract the name and address
        for contract_element in contract_elements:
            name_element = contract_element.find_element(By.XPATH, './/span[1]')
            address = contract_element.get_attribute('href')
            name = name_element.text.strip().rstrip(':').lower()
            contracts.append({"name": name, "address": address})
        
        return contracts

    def fetch_all_values(self):
        """Fetch the values of various parameters."""
        values = {
            "Price": self.fetch_price(),
            "Price Change": self.fetch_price_change(),
            "MarketCap": self.fetch_market_cap(),
            "MarketCap Change": self.fetch_market_cap_change(),
            "MarketCap Rank": self.fetch_market_cap_rank(),
            "Volume": self.fetch_volume(),
            "Volume Change": self.fetch_volume_change(),
            "Volume Rank": self.fetch_volume_rank(),
            "Circulating Supply": self.fetch_circulating_supply(),
            "Total Supply": self.fetch_total_supply(),
            "Diluted Market Cap": self.fetch_diluted_market_cap(),
            "Official Links": self.fetch_official_links(),
            "Social Links": self.fetch_social_links(),
            "Contracts": self.fetch_contracts(),
        }
        return values

    def extract_number(self, text):
        """Extract the first numerical value from a string."""
        match = re.search(r"[\d,]+(?:\.\d+)?", text)
        return match.group(0).replace(',', '') if match else text

    def print_values(self, values):
        """Print the values of various parameters."""
        for param, value in values.items():
            print(f"{param}: {value}")
        print()
    
    def monitor_and_report(self, interval=60):
        """Continuously monitor and report the values."""
        while True:
            # Fetch the values
            values = self.fetch_all_values()

            # Print the values
            self.print_values(values)

            # Wait for the specified interval
            time.sleep(interval)

if __name__ == '__main__':
# Define the URL to scrape
    url = "https://coinmarketcap.com/currencies/notcoin/"

# Create an instance of the scraper and start monitoring
    scraper = CoinMarketCapScraper(url, browser='firefox', headless=True)
    scraper.monitor_and_report(interval=0.1)  # Check every 5 minutes (300 seconds)
