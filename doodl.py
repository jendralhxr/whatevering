from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import sys
import time

def get_video_url(page_url):
    # Path to the GeckoDriver
    geckodriver_path = '/usr/local/bin/geckodriver'  # Adjust to your GeckoDriver path

    # Configure the WebDriver
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Run in headless mode
    
    # Initialize the WebDriver
    try:
        service = Service(executable_path=geckodriver_path)
        driver = webdriver.Firefox(service=service, options=firefox_options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        sys.exit(1)

    # Navigate to the page
    try:
        driver.get(page_url)
    except Exception as e:
        print(f"Error loading page: {e}")
        driver.quit()
        sys.exit(1)

    # Wait for the page to load and block or close ads
    try:
        # Example: Wait for a specific ad element to be present and try to close it
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ad-close-button')))
        ad_close_button = driver.find_element(By.CLASS_NAME, 'ad-close-button')
        ad_close_button.click()
    except Exception as e:
        print(f"Error handling ad: {e}")

    # Click the play button if present
    try:
        play_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.play-button-class')))
        play_button.click()
    except Exception as e:
        print(f"Error clicking play button: {e}")

    # Give some time for the video to load
    time.sleep(5)  # Adjust as necessary

    # Extract the video URL
    video_url = None
    try:
        video_element = driver.find_element(By.TAG_NAME, 'video')
        video_url = video_element.get_attribute('src')
    except Exception as e:
        print(f"Error finding video element: {e}")
    finally:
        driver.quit()

    return video_url

def download_video(video_url, output_file):
    # Check if the video URL is valid
    if not video_url:
        print("Invalid video URL.")
        return
    
    # Download the video
    try:
        response = requests.get(video_url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
            'Accept': 'video/mp4'
        }, stream=True)
        
        response.raise_for_status()  # Check for HTTP errors

        # Write to file
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"Download successful! File saved as {output_file}")
    except Exception as e:
        print(f"Download failed: {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python download_video.py <Page URL> <output_file>")
        sys.exit(1)

    page_url = sys.argv[1]
    output_file = sys.argv[2]

    # Get the video URL from the page
    video_url = get_video_url(page_url)

    # Download the video
    download_video(video_url, output_file)

if __name__ == "__main__":
    main()
