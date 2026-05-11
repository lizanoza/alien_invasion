from pathlib import Path

class GameStats:
    """Track statistics for alien invasion"""
    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset
        path = Path("alien_invasion_highscore.txt")
        contents = path.read_text()
        self.high_score = int(contents)

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit # Guarda cuantas vidas quedan
        self.score = 0
        self.level = 1