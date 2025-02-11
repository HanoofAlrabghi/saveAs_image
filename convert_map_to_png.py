import os
import time
import folium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image

def convert_HeatMap_to_image(data, image_name):
    riyadh_maps = folium.Map(location=[24.74, 46.69], zoom_start=10)
    # Prepare data for heatmap
    heat_data = list(zip(data.Latitude, data.Longitude))
    # Add the heatmap layer
    HeatMap(heat_data, radius=13, blur=10, min_opacity=0.4).add_to(riyadh_maps)
    #Step 1: Save Folium Map as an HTML File
    htmlfile = os.path.join("static/maps", image_name + ".html")
    riyadh_maps.save(htmlfile)
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
    pngfile = os.path.join("static/maps", image_name + ".png")
    driver.save_screenshot(pngfile)
    # Step 6: Close the Browser
    driver.quit()
    # Step 7: Crop the Image (Optional)
    pilImage = Image.open(pngfile)
    width, height = pilImage.size
    #target_height = 500
    # Crop the image: Keep full width, cut height to 500px from the top
    croppedImage = pilImage.crop((0, 0, width, height))
    croppedImage.save(pngfile)  # Save final cropped image
    return pngfile  
