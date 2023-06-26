class Song:
    class Play:
        def __init__(self, date, location, gap, position, show_length, set) -> None:
            self.date = date
            self.location = location
            self.gap = gap
            self.position = position
            self.show_length = show_length
            self.set = set

        def to_dict(self):
            return {
                "date": self.date,
                "location": self.location,
                "gap": self.gap,
                "position": self.position,
                "show_length": self.show_length,
                "set": self.set,
            }

    def __init__(self, name) -> None:
        self.name = name
        self.plays = []

    def add_play(self, date, location, gap, position, show_length, set):
        self.plays.add(self.Play(date, location, gap, position, show_length, set))
        return self

    def to_dict(self):
        return {"name": self.name, "plays": [play.to_dict for play in self.plays]}

    def load_from_dict(self, dict) -> None:
        self.name = dict["name"]
        play_dict = dict["plays"]
        self.plays = [
            Play(
                play["date"],
                play["location"],
                play["gap"],
                play["position"],
                play["show_length"],
                play["set"],
            )
            for play in play_dict
        ]
