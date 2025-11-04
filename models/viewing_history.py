class ViewingHistory:
    def __init__(self, history_id: int, customer_id: int, content_id: int,
                 watched_at: str, progress: float, duration_watched: int):
        if not (0.0 <= progress <= 1.0):
            raise ValueError("Progress must be between 0.0 and 1.0")
        self.history_id = history_id
        self.customer_id = customer_id
        self.content_id = content_id
        self.watched_at = watched_at
        self.progress = progress
        self.duration_watched = duration_watched

        def get_duration_watched(self) -> float:
            return self.duration_watched