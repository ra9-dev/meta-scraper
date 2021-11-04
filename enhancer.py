"""enhance product testimonials from youtube"""

import os
from json import loads

import pandas as pd
import requests

API_KEY = "AIzaSyANHt5BrCCcXTwGV_tD2lB1-PytKHAm_9g"
RELATIVE_ENHANCE_DIR_PATH = "nykaa/enhance/"
RELATIVE_SCRAP_DIR_PATH = "nykaa/scrap/"
YOUTUBE_SEARCH_API = "https://www.googleapis.com/youtube/v3/search"


def enhance(product):
    """GET VIDEO TESTIMONIALS FROM YOUTUBE"""
    print(f"Searching Testimonials For {product =}")
    req_params = {
        "part": "snippet",
        "q": f"{product['name']} review",
        "key": API_KEY,
        "regionCode": "IN",
        "type": "video",
        "order": "viewCount",
    }
    response = requests.get(url=YOUTUBE_SEARCH_API, params=req_params)
    if response.status_code != 200:
        print(response.content)
        return False

    testimonials = []
    for search_item in loads(response.content)["items"]:
        video_link = (
            f"https://www.youtube.com/watch?v={search_item['id']['videoId']}"
        )
        testimonials.append(
            {
                "link": video_link,
                "title": search_item["snippet"]["title"],
                "channel": search_item["snippet"]["channelTitle"],
                "thumbnails": search_item["snippet"]["thumbnails"],
            }
        )

    return testimonials


def process_csv(file_path):
    """GET PRODUCTS -> RUN ENHANCER"""
    print(f"READING from {file_path =}")
    products_data = pd.read_csv(file_path, usecols=["code", "name"])
    products_data = products_data.to_dict("records")
    enhanced = []
    failed = []
    for product in products_data:
        testimonials = enhance(product=product)
        if testimonials:
            product["testimonials"] = testimonials
            enhanced.append(product)
        else:
            failed.append(product)

    if len(enhanced) > 0:
        enhanced = pd.DataFrame(enhanced)
        file_name = file_path.split("/")[-1]
        dir_path = os.path.dirname(os.path.realpath(__file__))
        complete_file_path = os.path.join(
            dir_path, RELATIVE_ENHANCE_DIR_PATH, file_name
        )
        enhanced.to_csv(complete_file_path)
        print(
            f"{len(enhanced)} Enhanced Data is stored in `{complete_file_path}`."
        )

    if len(failed) > 0:
        failed = pd.DataFrame(failed)
        file_name = file_path.split("/")[-1].split(".")[0]
        file_name = f"{file_name}_failed.csv"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        complete_file_path = os.path.join(
            dir_path, RELATIVE_SCRAP_DIR_PATH, file_name
        )
        failed.to_csv(complete_file_path)
        print(f"{len(failed)} Failed URL(s) restored in `{file_path}`.")

    # remove file when processed
    try:
        os.remove(file_path)
        print("FILE PROCESSED. REMOVING THIS FILE")
    except OSError:
        pass


def process():
    """Get scrapped files to enhance"""
    print("PROCESSING STARTED !!")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, RELATIVE_SCRAP_DIR_PATH)
    for file in os.listdir(dir_path):
        filename = os.fsdecode(file)
        if not filename.endswith(".csv"):
            continue
        file_path = os.path.join(dir_path, filename)
        process_csv(file_path=file_path)


if __name__ == "__main__":
    process()
