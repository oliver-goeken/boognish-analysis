from song import Song
import pandas as pd


def load_data():
    song_df = pd.read_picle("data.pkl")
    song_dict = song_df.to_dict()

    print(song_dict)

    songs = [Song(dict) for dict in song_dict]

    return songs


if __name__ == "__main__":
    songs = load_data()

    print(songs[0].name)
