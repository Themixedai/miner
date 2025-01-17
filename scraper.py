from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.parse
from utils import get_base_domain, find_social_links
from pocketbase import send_to_pocketbase
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse
from furl import furl

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import urllib.parse
import time
from utils import get_base_domain, find_social_links
from pocketbase import send_to_pocketbase

# Define blacklisted domains and keywords
BLACKLISTED_DOMAINS = {"google.com", "opentable.com", "treatwell.de"}
BLACKLISTED_KEYWORDS = {"book"}

def scrape_google_maps(search_query):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) as driver:
        try:
            # Construct the Google Maps search URL
            encoded_query = urllib.parse.quote_plus(search_query)
            url = f"https://www.google.com/maps/search/{encoded_query}"
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="feed"]')))
            
            # Scroll to load all businesses
            scrollable_div = driver.find_element(By.CSS_SELECTOR, '[role="feed"]')
            previous_height = driver.execute_script('return arguments[0].scrollHeight', scrollable_div)
            while True:
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                time.sleep(2)
                new_height = driver.execute_script('return arguments[0].scrollHeight', scrollable_div)
                if new_height == previous_height:
                    break
                previous_height = new_height
            
            # Extract links to business pages
            business_links = driver.find_elements(By.CSS_SELECTOR, '[role="feed"] > div > div > a')
            links = [link.get_attribute('href') for link in business_links]
            
            for link in links:
                driver.get(link)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                title = driver.find_element(By.TAG_NAME, 'h1').text.strip()
                if not title:
                    continue
                
                # Extract the website using BeautifulSoup
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                website = next((a['href'] for a in soup.find_all('a', href=True) 
                                if not any(domain in a['href'] for domain in BLACKLISTED_DOMAINS)), None)
                if not website or any(keyword in website for keyword in BLACKLISTED_KEYWORDS):
                    continue
                
                base_domain = get_base_domain(website)
                social_links = find_social_links(base_domain)
                if social_links['instagram'] or social_links['facebook']:
                    send_to_pocketbase(title, base_domain, social_links['instagram'], social_links['facebook'])
        
        except Exception as e:
            print(f"Error processing query {search_query}: {e}")

def main():
search_queries = {
    "query1": "nagel studio in baden-württemberg",
    "query2": "nagel studio in bayern",
    "query3": "nagel studio in berlin",
    "query4": "nagel studio in brandenburg",
    "query5": "nagel studio in hessen",
    "query6": "nagel studio in mecklenburg-vorpommern",
    "query7": "nagel studio in niedersachsen",
    "query8": "nagel studio in nordrhein-westfalen",
    "query9": "nagel studio in rheinland-pfalz",
    "query10": "nagel studio in saarland",
    "query11": "nagel studio in sachsen",
    "query12": "nagel studio in sachsen-anhalt",
    "query13": "nagel studio in schleswig-holstein",
    "query14": "nagel studio in thüringen",
    "query15": "nagel studio in bremen",
    "query16": "nagel studio in hamburg",
    "query17": "nagel studio in aalen",
    "query18": "nagel studio in abensberg",
    "query19": "nagel studio in achern",
    "query20": "nagel studio in adelsdorf",
    "query21": "nagel studio in angermünde",
    "query22": "nagel studio in augsburg",
    "query23": "nagel studio in bad belzig",
    "query24": "nagel studio in bad doberan",
    "query25": "nagel studio in bad freienwalde",
    "query26": "nagel studio in bad homburg",
    "query27": "nagel studio in bad nauheim",
    "query28": "nagel studio in bad salzuflen",
    "query29": "nagel studio in bad soden am taunus",
    "query30": "nagel studio in bad wildbad",
    "query31": "nagel studio in bielefeld",
    "query32": "nagel studio in bonn",
    "query33": "nagel studio in braunschweig",
    "query34": "nagel studio in bremerhaven",
    "query35": "nagel studio in chemnitz",
    "query36": "nagel studio in cottbus",
    "query37": "nagel studio in dortmund",
    "query38": "nagel studio in dresden",
    "query39": "nagel studio in düsseldorf",
    "query40": "nagel studio in essen",
    "query41": "nagel studio in erfurt",
    "query42": "nagel studio in essen",
    "query43": "nagel studio in friedrichshain-kreuzberg",
    "query44": "nagel studio in freiburg im breisgau",
    "query45": "nagel studio in gießen",
    "query46": "nagel studio in göttingen",
    "query47": "nagel studio in görlitz",
    "query48": "nagel studio in habach",
    "query49": "nagel studio in halle (saale)",
    "query50": "nagel studio in hamburg",
    "query51": "nagel studio in hansestadt lübeck",
    "query52": "nagel studio in heidelberg",
    "query53": "nagel studio in heisenberg",
    "query54": "nagel studio in herford",
    "query55": "nagel studio in hohnstein",
    "query56": "nagel studio in jena",
    "query57": "nagel studio in kambs",
    "query58": "nagel studio in karlsruhe",
    "query59": "nagel studio in köln",
    "query60": "nagel studio in landshut",
    "query61": "nagel studio in leipzig",
    "query62": "nagel studio in lübeck",
    "query63": "nagel studio in mainz",
    "query64": "nagel studio in mannheim",
    "query65": "nagel studio in mönchengladbach",
    "query66": "nagel studio in münchen",
    "query67": "nagel studio in nürnberg",
    "query68": "nagel studio in oberhausen",
    "query69": "nagel studio in offenburg",
    "query70": "nagel studio in paderborn",
    "query71": "nagel studio in potsdam",
    "query72": "nagel studio in regensburg",
    "query73": "nagel studio in remscheid",
    "query74": "nagel studio in rostock",
    "query75": "nagel studio in saarbrücken",
    "query76": "nagel studio in stuttgart",
    "query77": "nagel studio in tübingen",
    "query78": "nagel studio in ulm",
    "query79": "nagel studio in wesel",
    "query80": "nagel studio in wiesbaden",
    "query81": "nagel studio in wuppertal",
    "query82": "nagel studio in würzburg",
    "query83": "nagel studio in zella-mehlis",
    "query84": "nagel studio in zittau",
    "query85": "nagel studio in zwickau",
    "query86": "nail salon in london",
    "query87": "nail salon in paris",
    "query88": "nail salon in rome",
    "query89": "nail salon in madrid",
    "query90": "nail salon in amsterdam",
    "query91": "nail salon in brussels",
    "query92": "nail salon in vienna",
    "query93": "nail salon in stockholm",
    "query94": "nail salon in copenhagen",
    "query95": "nail salon in dublin",
    "query96": "nail salon in lisbon",
    "query97": "nail salon in prague",
    "query98": "nail salon in budapest",
    "query99": "nail salon in zurich",
    "query100": "nail salon in helsinki",
    "query101": "nail salon in sofia",
    "query102": "nail salon in athens",
    "query103": "nail salon in bratislava",
    "query104": "nail salon in tallinn",
    "query105": "nail salon in vilnius",
    "query106": "nail salon in riga",
    "query107": "nail salon in belgrade",
    "query108": "nail salon in sarajevo",
    "query109": "nail salon in podgorica",
    "query110": "nail salon in skopje",
    "query111": "nail salon in tirana",
    "query112": "nail salon in oslo",
    "query113": "nail salon in bergen",
    "query114": "nail salon in reykjavik",
    "query115": "nail salon in amman",
    "query116": "nail salon in cyprus",
    "query117": "nail salon in malta",
    "query118": "nagel studio in mitte",
    "query119": "nagel studio in friedrichshain",
    "query120": "nagel studio in kreuzberg",
    "query121": "nagel studio in charlottenburg",
    "query122": "nagel studio in wilmersdorf",
    "query123": "nagel studio in spandau",
    "query124": "nagel studio in tempelhof",
    "query125": "nagel studio in neukölln",
    "query126": "nagel studio in steglitz",
    "query127": "nagel studio in zehlendorf",
    "query128": "nagel studio in treptow",
    "query129": "nagel studio in pankow",
    "query130": "nagel studio in lichtenberg",
    "query131": "nagel studio in reinickendorf",
    "query132": "nagel studio in schöneberg",
    "query133": "nagel studio in wedding",
    "query134": "nagel studio in bauernfeld",
    "query135": "nagel studio in alt-treptow",
    "query136": "nagel studio in biesdorf",
    "query137": "nagel studio in marzahn",
    "query138": "nagel studio in oberschöneweide",
    "query139": "nagel studio in plänterwald",
    "query140": "nagel studio in kladow",
    "query141": "nagel studio in müggelheim",
    "query142": "nagel studio in carlshorst",
    "query143": "nagel studio in frohnau",
    "query144": "nagel studio in köpenick",
    "query145": "nagel studio in haselhorst",
    "query146": "nagel studio in hakenfelde",
    "query147": "nagel studio in waldsiedlung",
    "query148": "nagel studio in märkisches viertel",
    "query149": "nagel studio in alt-templhof",
    "query150": "nagel studio in alt-moabit",
    
    
    # Note: The list can be expanded or refined as necessary.
}
    # Loop through the dictionary and scrape each query
    for query_name, search_query in search_queries.items():
        print(f"Processing {query_name}: {search_query}")
        scrape_google_maps(search_query)

if __name__ == "__main__":
    main()