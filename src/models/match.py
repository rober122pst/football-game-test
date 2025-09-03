from .teams import Team
from .players import Player
import random

class MatchState:
    def __init__(self, team_home: Team, team_away: Team) -> None:
        self.team_home = team_home
        self.team_away = team_away
        self.current_time = 0
        self.home_score = 0
        self.away_score = 0
        self.player_with_ball: Player = None
        self.team_with_ball: Team = None
        self.ball_position = (0, 0)
        self.events = []
        self.field_condition = 'dry'
        self.weather = 'rain'
        self.match_importance = 'normal'

        self._define_initial_possession()

    def _define_initial_possession(self):
        if random.random() < 0.5:
            self.team_with_ball = self.team_home
            self.player_with_ball = random.choice(self.team_home.players)
        else:
            self.team_with_ball = self.team_away
            self.player_with_ball = random.choice(self.team_away.players)

    def player_team(self, player):
        if player in self.team_home.players:
            return self.team_home
        else:
            return self.team_away