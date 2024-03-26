import requests
from bs4 import BeautifulSoup
import json


def get_author_details(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'lxml')
    fullname = soup.find('h3', class_='author-title').text.strip()
    born_date = soup.find('span', class_='author-born-date').text.strip()
    born_location = soup.find(
        'span', class_='author-born-location'
    ).text.strip()
    description = soup.find('div', class_='author-description').text.strip()

    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }


def scrape_quotes(soup, authors_urls):
    quotes = []
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        author_url = 'https://quotes.toscrape.com' + quote.find('a')['href']
        tags = [
            tag.text for tag in quote.find('div', class_='tags')
            .find_all('a', class_='tag')
        ]

        if author not in authors_urls:
            authors_urls[author] = author_url

        quotes.append(
            {'tags': tags,
             'author': author,
             'quote': text})
    return quotes


def scrape_all_quotes(initial_url):
    quotes = []
    authors_urls = {}
    url = initial_url

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes += scrape_quotes(soup, authors_urls)

        next_btn = soup.find('li', class_='next')
        if next_btn:
            url = 'https://quotes.toscrape.com' + next_btn.find('a')['href']
        else:
            url = None

    authors_details = [
        get_author_details(url) for url in authors_urls.values()
    ]

    return quotes, authors_details


def main():
    initial_url = 'https://quotes.toscrape.com/'
    quotes_data, authors_data = scrape_all_quotes(initial_url)

    # Writing quotes data to JSON file
    with open('quotes.json', 'w') as file:
        json.dump(quotes_data, file, indent=2, ensure_ascii=False)

    # Writing authors data to JSON file
    with open('authors.json', 'w') as file:
        json.dump(authors_data, file, indent=2, ensure_ascii=False)

    print("Data has been written to quotes.json and authors.json")


if __name__ == "__main__":
    main()
