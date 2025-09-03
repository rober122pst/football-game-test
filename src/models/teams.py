from dataclasses import dataclass, field
from .players import Player
from ..types.types import TaticalSetup, FORMATION_352, FORMATION_433, FORMATION_442 

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
    
    curr_formation = None
    avaliable_formation = {
        "4-4-2": FORMATION_442,
        "4-3-3": FORMATION_433,
        "3-5-2": FORMATION_352
    }
    curr_defensive_line = 20
    curr_offensive_line = 60
    team_width = 40

    def define_formation(self, formation_name: str):
        """Define a formação tática e posiciona os jogadores."""
        if formation_name in self.avaliable_formation[formation_name]:
            self.curr_formation = self.avaliable_formation[formation_name]

        # Posicionar jogadores nas posições base
        position_count = {}
        for player in self.players:
            position = player.position
            if position not in position_count:
                position_count[position] = 0

            player.define_positioning(self.curr_formation, position_count[position])
            position_count[position] += 1

    def adjust_compression(self, compression: float):
        """Ajusta o quão compacto o time joga (0 = muito aberto, 1 = muito fechado)"""
        for player in self.players:
            x_base, y_base = player.positioning

            field_centre_y = 0
            centre_distance = y_base - field_centre_y
            new_distance = centre_distance * (1 - compression * 0.5)
            new_y = field_centre_y + new_distance
            player.positioning = (x_base, y_base)

    def add_player(self, player: Player):
        self.players.append(player)
        
    def __str__(self) -> str:
        return f"Time: {self.name} - Tática: {self.tatics} - Jogadores: {len(self.players)}"


