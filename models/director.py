from typing import List

class Director():
    def __init__(self, director_id: int, full_name: str, birth_year: int, filmography: List[str]):
        self.director_id = director_id
        self.full_name = full_name
        self.birth_year = birth_year
        self.filmography = filmography

    def get_filmography(self) -> List[str]:
        return self.filmography

    def add_film(self, title: str) -> None:
        if title not in self.filmography:
            self.filmography.append(title)