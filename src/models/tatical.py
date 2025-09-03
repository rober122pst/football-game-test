from .players import Position

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

FORMACAO_442 = TaticalSetup("4-4-2", {
    Position.GOLEIRO: [(5.0, 30.0)],
    Position.ZAGUEIRO: [(15.0, 15.0), (15.0, 45.0), (20.0, 20.0), (20.0, 40.0)],
    Position.MEIA: [(35.0, 10.0), (35.0, 50.0), (45.0, 20.0), (45.0, 40.0)],
    Position.ATACANTE: [(75.0, 25.0), (75.0, 35.0)]
})