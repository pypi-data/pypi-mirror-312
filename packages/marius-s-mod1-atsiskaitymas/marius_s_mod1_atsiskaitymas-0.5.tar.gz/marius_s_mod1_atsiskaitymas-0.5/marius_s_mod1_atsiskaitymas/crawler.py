import requests
from lxml import html
from urllib.parse import urljoin
import time
import csv
import os
import sys


def crawling(site, timeout=10, format='list'):
    """
    Crawl articles from specified URL and return the article titles and associated image URLs.
    :param site:
        The site to crawl ('lrytas.lt' or 'kaunodiena.lt')
    :param timeout:
        The maximum time in seconds to run the crawl before stopping
    :param format:
        The format in which to return the data ('list' or 'csv')
    :return:
        List of tuples, where each tuple contains the article title and attached image URL
    """
    start_time = time.time()  #start the timer
    articles = []  #list to store crawled articles

    #defined site-specific XPaths for titles and images
    if site == 'lrytas.lt':
        url = 'https://www.lrytas.lt/'
        title_path = "//h2[contains(@class, 'text-base') and contains(@class, 'font-medium') and contains(@class, 'text-black-custom')]/a[1]/text()"
        image_path = "//div[contains(@class, 'rounded-[4px]')]/a/img/@src"

    elif site == 'kaunodiena.lt':
        url = 'https://kauno.diena.lt/'
        title_path = "//a[contains(@class, 'articles-list-title')]/text()"
        image_path = ".//div[contains(@class, 'articles-list-media')]//img"

    else:
        #raise an error if site is unsupported
        raise ValueError("Unsupported site, please choose 'https://www.lrytas.lt/' or 'https://kauno.diena.lt/'")

    try:
        response = requests.get(url)  #send a GET request to the website
        response.raise_for_status()  #raise an exception for bad HTTP responses
        tree = html.fromstring(response.content)  #parse HTML using lxml

        titles = tree.xpath(title_path) #extract titles
        images = tree.xpath(image_path) #extract images

        for title, img in zip(titles, images):
            if time.time() - start_time > timeout: #check if timeout has been exceeded
                print("Timeout reached - function stopped")
                break

            #article title handling for different formats
            if isinstance(title, str):
                article_title = title.strip()
            elif hasattr(title, 'text'):
                article_title = title.text.strip() if title.text else None
            else:
                article_title = None

            #skip articles with no title
            if not article_title:
                print("Skipping article with no title")
                continue

            #image URL handling for different formats
            if isinstance(img, str):
                image_url = img.strip()
            elif hasattr(img, 'get'):
                image_url = img.get("data-src") or img.get("src")
            else:
                image_url = None

            #convert to absolute URLS and filter out blank images
            if image_url and "blank.gif" not in image_url:
                image_url = urljoin(url, image_url)

            #add the titles and images to the list
            articles.append((article_title, image_url))

    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")

    except ValueError as value_error:
        print(f"Error: {value_error}")

    except Exception as error:
        print(f"An error occurred: {error}")

    finally:
        print("Crawling attempt finished")

    #return results based on chosen format
    if format == 'list':
        return articles
    elif format == 'csv':
        #CSV file creation/update
        csv_file = "articles.csv"
        file_exists = os.path.isfile(csv_file)
        existing_entries = set()

        #read existing entries to avoid duplicates
        if file_exists:
            with open(csv_file, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader, None)
                existing_entries.update(tuple(row) for row in reader)

        #filter out duplicates
        unique_articles = [article for article in articles if article not in existing_entries]

        #write new articles to CSV
        with open(csv_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Title", "Image URL"])

            writer.writerows(unique_articles)

        return "CSV file updated" if unique_articles else "No new articles found"
    else:
        raise ValueError("Unsupported format, please choose 'list' or 'csv'")


def crawl(site=None, timeout=None, format=None):
    """
    Runs the crawling process by validating input arguments and calling the crawling function.
    """
    #prioritize command-line arguments if they exist
    if len(sys.argv) == 4:
        site = sys.argv[1]
        try:
            timeout = int(sys.argv[2])
        except ValueError:
            print("Error: Timeout must be an integer")
            sys.exit(1)
        format = sys.argv[3]
    elif site is None or timeout is None or format is None:
        print("Usage: python main.py <site-URL> <timeout> <format>")
        print("Or provide arguments when calling the function")
        sys.exit(1)

        #validate site input
    if site not in ['lrytas.lt', 'kaunodiena.lt']:
        print("Error: Site must be 'lrytas.lt' or 'kaunodiena.lt'")
        sys.exit(1)

        #validate timeout input
    if not isinstance(timeout, int):
        print("Error: Timeout must be an integer")
        sys.exit(1)

        #validate format input
    if format not in ['list', 'csv']:
        print("Error: Format must be 'list' or 'csv'")
        sys.exit(1)

        # Call the crawling function with the arguments
    print(f"Running crawl for site: {site}")
    result = crawling(site=site, timeout=timeout, format=format)

    # Handle and display the results based on format chosen
    if format == 'list':
        for index, (title, image_url) in enumerate(result, start=1):
            print(f"{index}. {title}\nImage: {image_url}")
    elif format == 'csv':
        print(result)
