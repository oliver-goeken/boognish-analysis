from song import Song
import pandas as pd
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def load_data(file):
    song_df = pd.read_parquet(file)
    song_dict = song_df.to_dict(orient="records")

    songs = [Song(dict) for dict in song_dict]

    return songs


def get_user_input(prompt):
    print(prompt)
    print("> ", end="")
    return input()


def find_matching_song(user_input, songs):
    song_matches = []
    song_match = None

    for song in songs:
        if song.name.lower() == user_input:
            song_match = song
        elif fuzz.ratio(song.name.lower(), user_input) > 75:
            song_matches.append(song)

    if song_match:
        return song_match
    elif len(song_matches) == 0:
        print("Song not found!")
        return None
    else:
        for i in range(len(song_matches)):
            print("[" + str(i + 1) + "] - " + song_matches[i].name)

        while True:
            song_num = int(
                get_user_input(
                    "Which song did you mean? (input the corresponding number)"
                )
            )
            if song_num > 0 and song_num <= len(song_matches):
                return song_matches[song_num - 1]
            else:
                print("Please input a valid number.")


def main_loop(songs):
    analyzing = True

    while analyzing:
        user_input = get_user_input(
            "\n\n\nWhich Ween song would you like to analyze?"
        ).lower()

        song = find_matching_song(user_input, songs)

        years = int(
            get_user_input(
                'How many years would you like to analyze "' + song.name + '" over?'
            )
        )

        time_diff = time.localtime()
        time_diff_writeable = list(time_diff)
        time_diff_writeable[0] -= years
        time_diff = time.mktime(tuple(time_diff_writeable))

        gaps = []

        for play in song.plays:
            if time.mktime(time.strptime(play.date, "%m-%d-%Y")) > time_diff:
                gaps.append(int(play.gap))

        total_gap = 0
        for gap in gaps:
            total_gap += gap

        print(
            "The average gap for the past "
            + str(years)
            + ' years for the song "'
            + song.name
            + '" is:'
        )
        print(total_gap / len(gaps))


if __name__ == "__main__":
    songs = load_data("data.parquet")

    main_loop(songs)
