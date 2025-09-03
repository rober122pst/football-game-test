from dataclasses import dataclass, field
from .players import Player, Position

@dataclass
class Team:
    _id: int
    name: str
    coach_instructions: dict
    tatics: dict = "4-3-3" # ex 4-3-3, 4-4-2, 5-3-2
    harmony: int = 75
    moral: int = 80
    players: list = field(default_factory=list)
    setorial_strength: dict = field(default_factory=lambda:  {
        'attack': 0,
        'midfield': 0,
        'defense': 0,
        'goalkeeper': 0
    })
    
    def add_player(self, player: Player):
        self.players.append(player)
        
    def __str__(self) -> str:
        return f"Time: {self.name} - Tática: {self.tatics} - Jogadores: {len(self.players)}"


