"""scraps url from nykaa_urls file"""

import os
from urllib.parse import parse_qs, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

from add_url import validate_url_list

RELATIVE_NEW_DIR_PATH = "nykaa/new/"
RELATIVE_SCRAP_DIR_PATH = "nykaa/scrap/"


def scrap_nykaa(url):
    """Handles nykaa product page scrapping.
    We will have to customise this based on ecomm.
    """

    response = requests.get(url)
    if response.status_code != 200:
        # unreachable url
        print(f"{response.status_code =}")
        return False

    soup = BeautifulSoup(response.content, "html.parser")
    product_dom = soup.find_all("div", class_="css-11ayi09")
    # print(f"{product_dom =}")
    if not product_dom:
        # not a valid product page
        return False

    product_details = {}
    query_params = parse_qs(urlparse(url).query)
    # !Assumption this will be present in the url
    product_details["code"] = query_params["productid"][0]
    product_details["name"] = soup.body.h1.text
    # fetch category
    # category = soup.find("ul", class_="css-1uxnb1o")
    # print(f"{category =}")
    # print(f"{str(category) =}")
    # if category:
    #     category_2 = category.findChildren()
    #     # category_2 = category.find("name").find_parent("li")
    #     # , class_="css-46bku9")
    #     print(f"{category_2 =}")
    return product_details


def process_csv(file_path):
    """Get URLs -> Validate URLs -> Get Product Details -> Store"""
    print(f"READING from {file_path =}")
    urls = pd.read_csv(file_path)
    urls = urls["url"].tolist()
    valid_urls = validate_url_list(url_list=urls)
    non_product_urls = []

    products_data = []
    for url in valid_urls:
        print("\n-----------------------\n")
        print(f"Scrapping for {url =}")
        product_details = scrap_nykaa(url=url)
        if not product_details:
            print("NOT A PRODUCT PAGE")
            non_product_urls.append(url)
            continue

        products_data.append(product_details)
        print(f"{product_details =}")
        print("\n-----------------------\n")

    products_data = pd.DataFrame(products_data)
    print(products_data)
    if not products_data.empty:
        # print(f"Found {len(products_data)} Valid Products Data")
        file_name = file_path.split("/")[-1]
        dir_path = os.path.dirname(os.path.realpath(__file__))
        complete_file_path = os.path.join(
            dir_path, RELATIVE_SCRAP_DIR_PATH, file_name
        )
        products_data.to_csv(complete_file_path)
        print(
            f"{len(products_data)} URL(s) successfully added to `{complete_file_path}`."
            "Please run enhancer.py"
        )

    # TODO: Store and alert user that some urls are not valid

    # remove file when processed
    try:
        os.remove(file_path)
        print("FILE PROCESSED. REMOVING THIS FILE")
    except OSError:
        pass


def process():
    """Get new files to scrap/process"""
    print("PROCESSING STARTED !!")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, RELATIVE_NEW_DIR_PATH)
    for file in os.listdir(dir_path):
        filename = os.fsdecode(file)
        if not filename.endswith(".csv"):
            continue
        file_path = os.path.join(dir_path, filename)
        process_csv(file_path=file_path)


if __name__ == "__main__":
    process()
