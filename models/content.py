from typing import List
from .director import Director
from .genre import Genre

class Content:
    def __init__(self, content_id: int, title: str, description: str, release_year: int, duration: int):
        self.content_id = content_id
        self.title = title
        self.description = description
        self.release_year = release_year
        self.duration = duration
        self.rating: float = 0.0
        self.genres: List[Genre] = []
        self.directors: List[Director] = []

    def add_genre(self, genre: Genre) -> None:
        if genre not in self.genres:
            self.genres.append(genre)

    def add_director(self, director: Director) -> None:
        if director not in self.directors:
            self.directors.append(director)

    def update_rating(self, rating: float) -> None:
        self.rating = rating

    def get_info(self) -> dict:
        return {
            "id": self.content_id,
            "title": self.title,
            "year": self.release_year,
            "rating": self.rating,
            "genres": [g.name for g in self.genres],
            "directors": [d.full_name for d in self.directors]
        }

class Movie(Content):
    def __init__(self, content_id: int, title: str, description: str, release_year: int,
                 duration: int, is_premiere: bool=False):
        super().__init__(content_id, title, description, release_year, duration)
        self.is_premiere = is_premiere

        def mark_as_premiere(self) -> None:
            self.is_premiere = True

        def unmark_premiere(self) -> None:
            self.is_premiere = False


class Episode:
    def __init__(self, episode_id: int, series_id: int, season_number: int,
                 episode_number: int, title: str, duration: int):
        self.episode_id = episode_id
        self.series_id = series_id
        self.season_number = season_number
        self.episode_number = episode_number
        self.title = title
        self.duration = duration

    def get_full_title(self) -> str:
        return f"S{self.season_number:02d}E{self.episode_number:02d}: {self.title}"


class Series(Content):
    def __init__(self, contrent_id: int, title: str, description: str, release_year: int,
                 duration: int, seasons: int):
        super().__init__(contrent_id, title, description, release_year, duration)
        self.seasons = seasons
        self.episodes: List[Episode] = []

    def add_episode(self, episode: Episode) -> None:
        self.episodes.append(episode)

    def get_total_episodes(self) -> int:
        return len(self.episodes)

