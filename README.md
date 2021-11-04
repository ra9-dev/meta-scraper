# Product Metadata Enhancer

## Adding product data from external sources to your catalog

- Provide links to your ecommerce product page
- Follow the instructions in the README.md
- ✨ Get Enhanced product feed ✨

## Features and Assumptions

- For demo purposes, the program only accepts **_Nykaa product urls_**.
- Few validations are added to discard invalid urls or _non-Nykaa URLs_ initially.
- URLs added from Nykaa but not a valid product page will also be validated and discarded while processing.
- Adds video testimonials from youtube to your product feed (Currently containes _code, name_).
- Product feed is in csv format so can easily be accessed ahead.
- Since _for every step a different script_ is being used, this is **_failure resistant_**.

_Please Note:_

> The application required 3 different scripts to run
>
> _1. Adding urls_ > _2. Scrapping Nykaa Product Page (to get basic info)_ > _3. Get video testimonials from Youtube. (top 5)_
> This is done to make application for scalable in future and more error-proof today.
> Currently each script needs to be executed manually, in future a queue based trigger could be made to make it more seamless.
> For demo purposes, csv files have been used rather than a database to store database.
> Many functions/file handlers could be made generic and re-used, but were avoided due to lack of time.

## Future Scope

- Instead of taking data from user, data can be pulled from a catalog (if provided)
- Different scrappers can be added to accomodate different ecommerce.
- These videos/testimonials can be presented on client's ecommerce page so that users can see feedback of products.
- Based on youtube's description and comments we can also differentiate if the feedback is positive and promote the positive feedback more to attract more users.

## Setup Pre-requisites and Installation

Requires

- [Python](https://www.python.org/) v3.8+
- [Pip](https://pip.pypa.io) v21+

Clone the Repo and Install the dependencies.

```sh
$ cd meta-scrapper
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Congrats you're all set up. Let's start

## How to run

- Execute `add_url.py`

  ```sh
  $ python add_url.py
  ```

  An input terminal will open up. Feel free to use these inputs or get your own at [Nykaa](https://nykaa.com)

  ```
  Number of URL(s) you wish to add [Max 10]: 4
  Enter url 1:
      https://www.nykaa.com/personal-care/face/facewash/c/1387?ptype=lst&id=1387&root=nav_3&dir=desc&order=popularity
  Enter url 2:
      https://www.nykaa.com/lakme-blush-glow-kiwi-freshness-gel-face-wash-with-kiwi-extracts/p/457011?productId=457011&pps=1&skuId=457009
  Enter url 3:
      https://www.nykaa.com/tresemme-hairfall-defense-shampoo/p/7681?productId=7681&pps=5&skuId=401646
  Enter url 4:
      https://www.nykaa.com/wow-skin-science-onion-black-seed-oil-shampoo-300ml/p/587063?productId=587063&pps=6
  ```

  This adds the (valid) URLs into _nykaa/new_ directory as _time.csv_

- Execute `scrapper.py`

  ```sh
  $ python scrapper.py
  ```

  This scraps the info from (valid product) URLs into _nykaa/scrap_ as _time.csv_ and deletes the earlier file from _nykaa/new_ directory

- Finally execute `enhancer.py`

  ```sh
  $ python enhancer.py
  ```

  This search the scrapped data received in previous step on youtube and stores the top 5 links into product data as `testimonials` into the scrapped data and store the final data in _nykaa/enhance_ as _time.csv_. This also stores the data for those we don't find any result into _nykaa/scrap_ as _time_failed.csv_.

## Get In Touch

_In case of clarification/doubts please drop me an email at **rahul19ag@gmail.com**_
