class Club:
    def __init__(self, name, tags, descr, likes):
        self.name = name
        self.tags = tags
        self.descr = descr
        self.likes = likes

    def club_json(self):
        club_json = {
            'name': self.name ,
            'tags': self.tags ,
            'descr': self.descr ,
            'likes': self.likes
        }
        return club_json