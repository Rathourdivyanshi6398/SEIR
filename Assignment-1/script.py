import sys
import requests
from bs4 import BeautifulSoup

# check if url is given
if len(sys.argv) != 2:
    print("Please run the program like this:")
    print("python script.py <website_url>")
    sys.exit()

website_url = sys.argv[1]
browser_info = {
    "User-Agent": "Mozilla/5.0"
}

try:
    # Request the webpage
    page_data = requests.get(website_url, headers=browser_info)
    page_data.raise_for_status()

   # read the html page
    parsed_page = BeautifulSoup(page_data.text, "html.parser")


    # Print title
    if parsed_page.title is not None:
        print("Title of the Page:\n")
        print(parsed_page.title.text.strip())
    else:
        print("No title available.")


    # Print body text
    if parsed_page.body:
        print("\nMain Content:\n")
        print(parsed_page.body.get_text("\n", strip=True))

    # Print all links
    print("\nLinks Found on Page:\n")
    for anchor_tag in parsed_page.find_all("a"):
        link_address = anchor_tag.get("href")
        if link_address:
            print(link_address)

except requests.exceptions.RequestException as error:
    print("Something went wrong while accessing the page:")

    print(error)
