import os
import time
import folium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image

def convert_map_png(folium_map, file_name):
    mapName = file_name
    # Step 1: Save Folium Map as an HTML File
    htmlfile = mapName + ".html"
    folium_map.save(htmlfile)
    # Step 2: Set Up Selenium with Chromedriver (Google Chrome)
    chrome_path = os.path.join(os.getcwd(), "chromedriver.exe")  # Ensure correct path
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--window-size=1024x768")  # Ensure correct map size
    service = Service(chrome_path)
    driver = webdriver.Chrome(service=service, options=options)
    # Step 3: Open the HTML File in Chrome
    file_url = f"file:///{os.path.abspath(htmlfile)}"
    driver.get(file_url)
    # Step 4: Wait for the Page to Load (Ensure JavaScript Loads)
    time.sleep(3)  # Wait for full map rendering
    # Step 5: Take Screenshot & Save as PNG
    pngfile = mapName + ".png"
    driver.save_screenshot(pngfile)
    # Step 6: Close the Browser
    driver.quit()
    # Step 7: Crop the Image (Optional)
    pilImage = Image.open(pngfile)
    width, height = pilImage.size
    left, top, right, bottom = 0, 0, width, height
    croppedImage = pilImage.crop((left, top, right, bottom))
    croppedImage.save(pngfile)  # Save final cropped image

    return pngfile  
