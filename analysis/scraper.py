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


def parse_song_data(URL):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
    }

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    song = Song(soup.find("h1").getText().split("by Ween")[0])

    table = soup.find("table", class_="main-table")
    play_history = table.find_all("tr", class_="bg_b") + table.find_all(
        "tr", class_="bg_a"
    )

    for play in play_history:
        data = play.find_all("td")

        if len(data) > 8:
            del data[0]

        play_date = data[1].getText().strip()
        play_loc = data[2].getText().strip()
        try:
            play_gap = data[3].getText().strip()
        except:
            play_gap = 0
        play_pos_size = data[4].getText().strip().split(" of ")
        print("-" + song.name + "- " + data[4].getText().strip())
        play_pos = play_pos_size[0]
        play_len = play_pos_size[1]
        play_set = data[5].getText().strip()

        song.add_play(play_date, play_loc, play_gap, play_pos, play_len, play_set)

    song.sort_plays()

    return song


if __name__ == "__main__":
    song_links = []

    URL = "https://brownbase.org/song_list.php?band=Ween&s={}&p=4&sort=2&ascDesc=DESC#table_top"
    URL_SORT = "&sort=1&ascDesc=ASC#table_top"
    URL_BASE = "https://brownbase.org/"
    page_number = 0

    while True:
        links = get_song_links(URL.format(page_number))

        if links == False:
            break
        else:
            song_links += links

        page_number += 100

    songs = []

    for song_link in song_links:
        songs.append(parse_song_data(URL_BASE + song_link + URL_SORT))

    songs = sorted(songs, key=lambda song: song.name)

    song_dict = [song.to_dict() for song in songs]
    song_df = pd.DataFrame(song_dict)
    song_df.to_parquet("data.parquet")
