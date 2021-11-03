"""add url to urls file"""

import os
import sys
import time

import pandas as pd
from validators import url as url_validator

DOMAIN_PREFIX = "https://www.nykaa.com/"
RELATIVE_DIR_PATH = "nykaa/new/"


def take_input():
    """takes n URLs from user"""
    try:
        size = int(input("Number of URL(s) you wish to add [Max 10]: "))
        if size > 10:
            raise ValueError
    except ValueError:
        print("Invalid number given. ABORTING !!")
        sys.exit(1)

    values = [input(f"Enter url {_+1}: ") for _ in range(size)]
    return values


def validate_url_list(url_list):
    """validates input urls"""
    print("VALIDATING URL(s) !!")
    # get unique urls
    url_list = list(set(url_list))
    # start validation process
    invalid_urls = []
    non_nykaa_urls = []
    validated_urls = []
    for url in url_list:
        url = url.lower()
        if not url_validator(url):
            invalid_urls.append(url)
        elif not url.startswith(DOMAIN_PREFIX):
            non_nykaa_urls.append(url)
        else:
            validated_urls.append(url)

    print("VALIDATION COMPLETE. REPORT: ")
    print(f"{len(url_list)} UNIQUE URLs received")
    print(f"{len(invalid_urls)} INVALID URL(s): {invalid_urls}")
    print(f"{len(non_nykaa_urls)} NON NYKAA URL(s): {non_nykaa_urls}")
    print(f"{len(validated_urls)} VALID URL(s): {validated_urls}")

    return validated_urls


def write_to_file(valid_url_list):
    """write valid urls to the csv file"""
    if not valid_url_list:
        print("No Valid URL(s) to add. ABORTING !!")
        sys.exit(1)

    file_name = f"{str(int(time.time()))}.csv"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    complete_file_path = os.path.join(dir_path, RELATIVE_DIR_PATH, file_name)
    # print(complete_file_path)
    url_df = pd.DataFrame({"url": valid_url_list})
    # print(url_df)
    url_df.to_csv(complete_file_path)
    print(
        f"{len(valid_url_list)} URL(s) successfully added to `{complete_file_path}`. Please run scrapper.py"
    )


if __name__ == "__main__":
    input_values = take_input()
    valid_urls = validate_url_list(url_list=input_values)
    write_to_file(valid_url_list=valid_urls)
