import requests
from bs4 import BeautifulSoup
import time
import os


def get_first_google_search(query, prefix='', class_identifier='egMi0') -> str:
    """Get the link for the first Google search result.

    Input is a .txt file containing the search query. The input should
    be named google-service-input.txt and be located in the same directory.

    Args:
        query: the google search query
        prefix: prefix to prepend to google search
        class_identifier: used to specify location of google search within
            the HTML. Recommended to keep default value unless Google
            changes the identifier.

    Returns:
        str: link of first google search result

    """
    query = query.replace('&', ' ')
    google_search = prefix + query
    google_search_url = "https://www.google.com/search?q=" + google_search

    webpage = requests.get(google_search_url)
    soup = BeautifulSoup(webpage.content, 'html.parser')

    top_result = soup.find(attrs={'class': class_identifier})
    link = top_result.find('a')['href']
    link = link.split('/url?q=')[1].split('&')[0]

    return link


def lyrics_scraper(url):
    """
    Scrape lyrics from Genius website URL.

    Args:
        url: URL for Genius song lyrics page

    Returns:
        string: song lyrics

    """
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, 'html.parser')

    lyrics_list = soup.find_all(attrs={'data-lyrics-container': 'true'})
    combined_lyrics = ''

    for lyrics in lyrics_list:
        for br in lyrics.find_all('br'):
            br.replace_with('\n')
        combined_lyrics += lyrics.text + '\n'

    return combined_lyrics


if __name__ == "__main__":
    while True:
        print("Waiting for file...")
        while True:
            try:
                with open('lyrics-service-input.txt') as file:
                    lyrics_service_input = file.read()
            except FileNotFoundError:
                time.sleep(2)
            else:
                print("File processing...")
                os.remove('lyrics-service-input.txt')
                break

        lyrics_url = get_first_google_search(lyrics_service_input, prefix="genius ")
        lyrics_text = lyrics_scraper(lyrics_url)

        with open('lyrics-service-output.txt', 'w', encoding='utf-8') as lyrics_file:
            lyrics_file.write(lyrics_text)

        print("Finished processing file\n")
