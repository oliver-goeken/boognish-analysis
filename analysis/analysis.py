from song import Song
import pandas as pd


def load_data():
    song_df = pd.read_parquet("data.parquet")
    song_dict = song_df.to_dict()
    print(song_dict)

    return None


if __name__ == "__main__":
    songs = load_data()
