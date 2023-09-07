import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote

# Prompt the user for the URL of the webpage to scrape
url = input("Enter the URL of the webpage to scrape: ")

# Initialize a web driver (if needed, e.g., for JavaScript-heavy pages)
# Uncomment this section if you need to use Selenium
# driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
# driver.get(url)
# html = driver.page_source

# If you don't use Selenium, you can use requests to fetch the page
response = requests.get(url)
html = response.text

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Prompt the user for the directory to save downloaded images
download_directory = input("Enter the directory to save downloaded images: ")
os.makedirs(download_directory, exist_ok=True)

# Prompt the user for how many images they want to download
num_images_to_download = int(input("Enter the number of images to download: "))

# Find and download images
img_tags = soup.find_all('img')
downloaded_count = 0

for img_tag in img_tags:
    img_url = img_tag.get('src')
    if not img_url or downloaded_count >= num_images_to_download:
        break

    # Create an absolute image URL if it's a relative URL
    img_url = urljoin(url, img_url)

    # Get the image content
    img_response = requests.get(img_url)

    # Extract the image file name from the URL and sanitize it
    img_name = os.path.basename(urlparse(unquote(img_url)).path)
    img_path = os.path.join(download_directory, img_name)

    # Save the image to the download directory
    with open(img_path, 'wb') as img_file:
        img_file.write(img_response.content)
        print(f"Downloaded: {img_name}")
        
    downloaded_count += 1

# Close the web driver (if used)
# Uncomment this section if you used Selenium
# driver.quit()
