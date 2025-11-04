class Genre:
    def __init__(self, genre_id: int, name: str, description: str = ""):
        self.genre_id = genre_id
        self.name = name
        self.description = description