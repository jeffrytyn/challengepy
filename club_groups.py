class Club:
    """
    Creating a Club object
    """
    def __init__(self, name, tags, descr, likes):
        self.name = name
        self.tags = tags
        self.descr = descr
        self.likes = likes
    """
    Represent Club object in a format to be added to JSON file
    """
    def club_json(self):
        club_json = {
            'name': self.name ,
            'tags': self.tags ,
            'descr': self.descr ,
            'likes': self.likes
        }
        return club_json