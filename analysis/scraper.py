import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape(URL):
    HEADER = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
    }

    page = requests.get(URL, headers=HEADER)
    soup = BeautifulSoup(page.content, "html.parser")

    return soup


def get_song_links(URL_BASE):
    URL_SONGS = "song_list.php?band=Ween&s={}&p=4&sort=2&ascDesc=DESC#table_top"

    page_number = 0
    song_links = []
    while True:
        links_page = scrape(URL_BASE + URL_SONGS.format(page_number))

        if any(
            error.getText() == "Ween did not play any songs in "
            for error in links_page.findAll("h3", class_="error")
        ):
            break
        else:
            songs = links_page.find_all("tr", class_="bg_b") + links_page.find_all(
                "tr", class_="bg_a"
            )

            for song in songs:
                if song.find("td", class_="mo-center").getText() == "by Ween":
                    song_links.append(
                        song.find("td", class_="mo-bigger").find("a")["href"]
                    )

            page_number += 100

    return song_links


def convert_date(date):
    date_arr = date.split("-")

    return date_arr[2] + date_arr[0] + date_arr[1]


def get_song_data(URL_BASE, song_links):
    songs = []

    for link in song_links:
        song_page = scrape(URL_BASE + link)
        song = {"name": song_page.find("h1").getText().split("by Ween")[0], "plays": []}

        main_table = song_page.find("table", class_="main-table")
        play_history = main_table.find_all("tr", class_="bg_b") + main_table.find_all(
            "tr", class_="bg_a"
        )

        for play in play_history:
            play_data = {
                "date": "",
                "location": "",
                "gap": "",
                "position": "",
                "show_length": "",
                "set": "",
            }

            info = play.find_all("td")
            if len(info) > 8:
                del info[0]

            info = [line.getText().strip() for line in info]

            play_data["date"] = info[1]
            play_data["location"] = info[2]
            pos_and_len = info[4].split(" of ")
            play_data["position"] = pos_and_len[0]
            play_data["show_length"] = pos_and_len[1]
            play_data["set"] = info[5]
            if info[3]:
                play_data["gap"] = info[3]
            else:
                play_data["gap"] = 0

            song["plays"].append(play_data)

            print(song["name"] + " -- " + play_data["date"])

        song["plays"] = sorted(
            song["plays"], key=lambda play: convert_date(play["date"])
        )

        songs.append(song)

    return songs


if __name__ == "__main__":
    URL_BASE = "https://brownbase.org/"

    song_links = get_song_links(URL_BASE)
    songs = get_song_data(URL_BASE, song_links)

    print(len(songs) + " songs scraped")

    song_df = pd.DataFrame(songs)
    song_df.to_parquet("data.parquet")
