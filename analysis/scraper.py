import requests
from bs4 import BeautifulSoup
import pandas as pd
from song import Song


def get_song_links(URL):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
    }

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    errors = soup.findAll("h3", class_="error")

    for error in errors:
        if error.getText() == "Ween did not play any songs in ":
            return False

    song_links = []

    songs = soup.find_all("tr", class_="bg_b") + soup.find_all("tr", class_="bg_a")

    for song in songs:
        if song.find_all("td", class_="mo-center")[0].getText() == "by Ween":
            song_links.append(
                song.find_all("td", class_="mo-bigger")[0].find("a")["href"]
            )

    return song_links


def parse_song_data():
    pass


if __name__ == "__main__":
    song_links = []

    URL = "https://brownbase.org/song_list.php?band=Ween&s={}&p=4&sort=2&ascDesc=DESC#table_top"
    URL_sort = "&sort=1&ascDesc=ASC#table_top"
    page_number = 0

    while True:
        links = get_song_links(URL.format(page_number))

        if links == False:
            break
        else:
            song_links += links

        page_number += 100

    songs = [Song("A Tear for Eddie").add_play(12, "here", 5, 6, 27, "Main")]

    song_dict = [song.to_dict() for song in songs]
    print(song_dict[0])
    song_df = pd.DataFrame(song_dict)
    song_df.to_pickle("data.pkl")
