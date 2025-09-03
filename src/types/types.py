from enum import Enum

class PlayerState(Enum):
    ATTACKING = "Atacando"
    DEFENDING = "Defendendo"
    MARKING = "Marcando"
    WITH_POSSESSION = "Com a posse"
    WITHOUT_POSSESSION = "Sem a posse"
    LOOKING_FOR_POSITION = "Procurando posição"

class Position(Enum):
    GOALKEEPER = "GK"
    CENTRE_BACK = "CB"
    L_BACK = "LB"
    R_BACK = "RB"
    L_WING_BACK = "LWB"
    R_WING_BACK = "RWB"

    CENTRAL_DEFENSE_MID = "CDM"
    CENTRAL_MIDFIELDER = "CM"
    L_CENTRAL_MID = "LCM"
    R_CENTRAL_MID = "RCM"
    L_MIDFILDER = "LDM"
    CENTRAL_ATTACK_MID = "CAM"

    LEFT_WINGER = "LW"
    RIGHT_WINGER = "RW"
    SECOND_STRIKER = "SS"
    CENTRE_FOWARD = "CF"
    STRIKER = "ST"

class Personality(Enum):
    LEADER = "Líder"
    INDIVIDUALIST = "Individualista"
    UNSTABLE = "Instável"
    COLD_IN_FINALS = "Frio em Finais"
    GOAL_SCORER = "Artilheiro"


class TaticalSetup:
    def __init__(self, name: str, positions: dict):
        self.name = name
        self.positions = positions # {posição: [(x, y), ...]}
        self.special_instructions = {}

    def get_base_position(self, position: Position, index: int = 0) -> tuple:
        """Retorna a posição base para um jogador de determinada função"""
        if position in self.positions:
            positions = self.positions[position]
            if index < len(positions):
                return positions[index]
        return (0, 0)

FORMATION_442 = TaticalSetup("4-4-2", {
    Position.GOALKEEPER: [(5.0, 30.0)],
    Position.CENTRE_BACK: [(15.0, 15.0), (15.0, 45.0), (20.0, 20.0), (20.0, 40.0)],
    Position.CENTRAL_ATTACK_MID: [(35.0, 10.0), (35.0, 50.0), (45.0, 20.0), (45.0, 40.0)],
    Position.STRIKER: [(75.0, 25.0), (75.0, 35.0)]
})
FORMATION_433 = TaticalSetup("4-3-3", {
    Position.GOALKEEPER: [(5.0, 30.0)],
    Position.CENTRE_BACK: [(15.0, 15.0), (15.0, 45.0), (20.0, 20.0), (20.0, 40.0)],
    Position.CENTRAL_ATTACK_MID: [(35.0, 10.0), (35.0, 50.0), (45.0, 20.0), (45.0, 40.0)],
    Position.STRIKER: [(75.0, 25.0), (75.0, 35.0)]
})
FORMATION_352 = TaticalSetup("3-5-2", {
    Position.GOALKEEPER: [(5.0, 30.0)],
    Position.CENTRE_BACK: [(15.0, 15.0), (15.0, 45.0), (20.0, 20.0)],
    Position.CENTRAL_ATTACK_MID: [(35.0, 10.0), (35.0, 50.0), (45.0, 20.0)],
    Position.STRIKER: [(75.0, 25.0), (75.0, 35.0)]
})
