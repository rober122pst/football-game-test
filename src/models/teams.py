from dataclasses import dataclass
from players import Player, Position

@dataclass
class Team:
    _id: int
    name: str
    coach_instructions: dict
    tatics: dict = "4-3-3" # ex 4-3-3, 4-4-2, 5-3-2
    harmony: int = 75
    moral: int = 80
    players = []
    setorial_strength = {
        'attack': 0,
        'midfield': 0,
        'defense': 0,
        'goalkepper': 0
    }
    
    def add_player(self, player: Player):
        self.players.append(player)
        
    def __str__(self) -> str:
        return f"Time: {self.name} - Tática: {self.tatics} - Jogadores: {len(self.players)}"

jogador1 = Player(1, "Rober", Position.STRIKER,
    {
        "positioning": 20,
        "finishing": 10,
        "long_shot": 12,
        "heading": 20,
        "dribbling": 20,
        "crossing": 20,
        "long_pass": 18,
        "short_pass": 16,
        "ball_control": 10,
        "curve": 10,
        "tackling": 20,
        "interceptions": 12,
        "marking": 11,
        "sliding_tackle": 18,
        "pressure": 9,
        "reflexes": 19,
        "placing": 17,
        "goalkeeping": 19
    },
    {
        "velocity": 15,
        "acceleration": 5,
        "strength": 17,
        "stamina": 16,
        "impulse": 17,
        "balance": 16
    },
    {
        "vision": 6,
        "composition": 16,
        "decision": 15,
        "lider": 12,
        "agression": 4,
        "concentration": 17,
        "composure": 17
    })

sport_recife = Team(87, "Sport Recife", {})
sport_recife.add_player(jogador1)
print(sport_recife)
    