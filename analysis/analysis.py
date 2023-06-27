from song import Song
import pandas as pd


def load_data():
    song_df = pd.read_parquet("data.parquet")
    song_dict = song_df.to_dict(orient="records")

    songs = [Song(dict) for dict in song_dict]

    return songs


if __name__ == "__main__":
    songs = load_data()

    for song in songs:
        print(song.name)
