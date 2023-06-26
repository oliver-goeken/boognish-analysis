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

    def __init__(self, data) -> None:
        if type(data) == dict:
            self.name = data["name"]
            play_dict = data["plays"]
            self.plays = [
                self.Play(
                    play["date"],
                    play["location"],
                    play["gap"],
                    play["position"],
                    play["show_length"],
                    play["set"],
                )
                for play in play_dict
            ]
        else:
            self.name = data
            self.plays = []

    def add_play(self, date, location, gap, position, show_length, set):
        self.plays.append(self.Play(date, location, gap, position, show_length, set))
        return self

    def to_dict(self):
        return {"name": self.name, "plays": [play.to_dict() for play in self.plays]}

    def sort_plays(self):
        self.plays = sorted(
            self.plays,
            key=lambda play: play.date.split("-")[2]
            + play.date.split("-")[0]
            + play.date.split("-")[1],
        )
