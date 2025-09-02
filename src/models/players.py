from enum import Enum
from dataclasses import dataclass
from ..core.decision_tree import DecisionNode
from ..core.odds import simulate_shoot_precision, simulate_pass

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

@dataclass
class Player:
    """Classe do jogador. Todos os seus dados e atributos + funções extras"""
    # TODO limitar limite de overall mesmo após o init
    _id: int
    name: str
    position: Position
    technique_attr: dict
    fisical_attr: dict
    mental_attr: dict
    positioning: tuple = (0, 0)

    current_state = PlayerState.WITHOUT_POSSESSION
    moral = 50 # 0 a 100
    fisical_fitness = 100 # 0 a 100
    injury = 5 # 0 a 100
    experience = 0
    personality = []
    

    def __post_init__(self):
        all_attr = self.technique_attr
        all_attr.update(self.fisical_attr)
        all_attr.update(self.mental_attr)

        for attr in all_attr.values():
            if not 0 <= attr <= 20:
                raise ValueError("Atributo maior que o valor permitido (1 a 20)")
            
    def calculate_overall(self, position: Position, weights_by_position=None, default_missing=10):
        """
        Calcula o overall (1-99) de um jogador a partir dos atributos.
        - attributes: dicionário com chaves de categoria (fisical, technique, mental) contendo atributos.
        - position: Posição do jogador (Enum Position).
        - weights_by_position: dict opcional com pesos por posição (cada peso deve somar 1.0, será normalizado se não somar).
        - default_missing: valor usado quando um atributo esperado não existir (padrão 10).
        Retorna um inteiro entre 1 e 99.
        """

        # Flatten dos atributos (fisical, technique, mental -> chaves únicas)
        flat = self.technique_attr
        flat.update(self.fisical_attr)
        flat.update(self.mental_attr)

        default_weights = {
            "GK": {
                "reflexes": 0.30, "goalkeeping": 0.30, "placing": 0.12, "positioning": 0.08,
                "concentration": 0.07, "composure": 0.05, "short_pass": 0.03, "strength": 0.03, "balance": 0.02
            },
            "CB": {
                "marking": 0.22, "interceptions": 0.20, "tackling": 0.18, "positioning": 0.12,
                "heading": 0.10, "strength": 0.08, "short_pass": 0.05, "concentration": 0.03, "composure": 0.02
            },
            "LB": {
                "stamina": 0.15, "acceleration": 0.13, "velocity": 0.12, "tackling": 0.12,
                "marking": 0.12, "crossing": 0.12, "short_pass": 0.07, "positioning": 0.06, "composure": 0.03
            },
            "RB": {
                "stamina": 0.15, "acceleration": 0.13, "velocity": 0.12, "tackling": 0.12,
                "marking": 0.12, "crossing": 0.12, "short_pass": 0.07, "positioning": 0.06, "composure": 0.03
            },
            "LWB": {
                "stamina": 0.16, "acceleration": 0.14, "velocity": 0.12, "crossing": 0.15,
                "dribbling": 0.10, "short_pass": 0.10, "tackling": 0.08, "positioning": 0.07, "composure": 0.04
            },
            "RWB": {
                "stamina": 0.16, "acceleration": 0.14, "velocity": 0.12, "crossing": 0.15,
                "dribbling": 0.10, "short_pass": 0.10, "tackling": 0.08, "positioning": 0.07, "composure": 0.04
            },
            "CDM": {
                "interceptions": 0.20, "tackling": 0.18, "positioning": 0.14, "short_pass": 0.12,
                "vision": 0.10, "stamina": 0.10, "composure": 0.08, "strength": 0.05, "concentration": 0.03
            },
            "CM": {
                "vision": 0.18, "short_pass": 0.18, "long_pass": 0.12, "decision": 0.12,
                "stamina": 0.11, "composure": 0.09, "dribbling": 0.07, "positioning": 0.07, "concentration": 0.06
            },
            "LCM": {
                "vision": 0.17, "short_pass": 0.17, "long_pass": 0.12, "decision": 0.12,
                "stamina": 0.11, "composure": 0.09, "dribbling": 0.08, "positioning": 0.07, "concentration": 0.07
            },
            "RCM": {
                "vision": 0.17, "short_pass": 0.17, "long_pass": 0.12, "decision": 0.12,
                "stamina": 0.11, "composure": 0.09, "dribbling": 0.08, "positioning": 0.07, "concentration": 0.07
            },
            "LDM": {
                "interceptions": 0.18, "tackling": 0.18, "positioning": 0.15, "short_pass": 0.12,
                "stamina": 0.12, "strength": 0.08, "composure": 0.07, "concentration": 0.05, "vision": 0.05
            },
            "CAM": {
                "vision": 0.165, "short_pass": 0.155, "dribbling": 0.142, "decision": 0.122,
                "long_shot": 0.102, "finishing": 0.082, "positioning": 0.082, "composure": 0.07
            },
            "LW": {
                "dribbling": 0.22, "acceleration": 0.16, "velocity": 0.14, "crossing": 0.12,
                "finishing": 0.12, "short_pass": 0.08, "positioning": 0.07, "ball_control": 0.06, "composure": 0.03
            },
            "RW": {
                "dribbling": 0.22, "acceleration": 0.16, "velocity": 0.14, "crossing": 0.12,
                "finishing": 0.12, "short_pass": 0.08, "positioning": 0.07, "ball_control": 0.06, "composure": 0.03
            },
            "SS": {
                "finishing": 0.22, "dribbling": 0.16, "positioning": 0.14, "acceleration": 0.12,
                "velocity": 0.10, "short_pass": 0.08, "ball_control": 0.08, "composure": 0.05, "vision": 0.05
            },
            "CF": {
                "finishing": 0.28, "positioning": 0.18, "heading": 0.12, "strength": 0.10,
                "acceleration": 0.08, "velocity": 0.07, "short_pass": 0.06, "ball_control": 0.06, "composure": 0.05
            },
            "ST": {
                "finishing": 0.30, "positioning": 0.18, "acceleration": 0.12, "velocity": 0.12,
                "heading": 0.08, "strength": 0.07, "ball_control": 0.06, "composure": 0.04, "short_pass": 0.03
            }
        }

        weights_by_position = weights_by_position or default_weights

        pos = position.value

        pos_weights = weights_by_position.get(pos, weights_by_position.get('CM'))

        s = sum(pos_weights.values())
        if s <= 0:
            raise ValueError("Pesos inválidos para a posição.")
        pos_weights = {k: v / s for k, v in pos_weights.items()}

        total = 0.0
        for attr, w in pos_weights.items():
            val = flat.get(attr, default_missing)  # se faltar, usa default
            # limita o valor pra evitar outliers (1..20)
            if val < 1: val = 1
            if val > 20: val = 20
            total += w * (val / 20.0)

        # escala para 1..99 e arredonda
        overall = round(total * 99)
        overall = max(1, min(99, int(overall)))
        return overall
    
    def update_fisical_fitness(self, fixture_intensit) -> int:
        """Diminui a forma fisica 10% de acordo com a intensidade da partida"""
        self.fisical_fitness * fixture_intensit * .1
        if self.fisical_fitness <= 0:
            self.fisical_fitness = 0

    def decide_action(self, game_state):
        """Decide a ação do jogador baseado no estado do jogo"""
        tree = DecisionNode('with_ball', filhos=[
            DecisionNode(value='yes', filhos=[
                DecisionNode('in_goal', filhos=[
                    DecisionNode(value='yes', action=lambda a: simulate_shoot_precision(self.technique_attr['finishing'], a['derivation'])),
                    DecisionNode(value='no', filhos=[
                        DecisionNode('friend_free', filhos=[
                            DecisionNode(value='yes', action=lambda a: simulate_pass(self.technique_attr['short_pass'], a['distance'], a['pression'], a['stadium_codition'])),
                            DecisionNode(value='no', action=None)
                        ])
                    ])
                ]),
            ]),
            DecisionNode(value='no', filhos=[
                DecisionNode('team_with_possession', filhos=[
                    DecisionNode(value='yes', action=None),
                    DecisionNode(value='no', action=None)
                ])
            ])
        ])
        
        tree.classificar(game_state)
        return "shoot"
        # if self.with_ball(game_state):
        #     self.current_state = PlayerState.WITH_POSSESSION
        # elif self.team_with_ball(game_state):
        #     self.current_state = PlayerState.ATTACKING
        # elif not self.team_with_ball(game_state):
        #     self.current_state = PlayerState.DEFENDING
            
        # if self.current_state == PlayerState.WITH_POSSESSION:
        #     self.decide_with_ball(game_state)
        # elif self.current_state == PlayerState.ATTACKING:
        #     self.decide_attacking_without_ball(game_state)
        # elif self.current_state == PlayerState.DEFENDING:
        #     self.decide_defending_without_ball(game_state)

    def decide_with_ball(self, game_state):
        """Decide a ação do jogador quando está com a bola"""
        if self.can_shoot(game_state):
            print(f"{self.name} decidiu chutar!")
        elif self.can_pass(game_state):
            print(f"{self.name} decidiu passar!")
        elif self.can_dribble(game_state):
            print(f"{self.name} decidiu driblar!")
        else:
            print(f"{self.name} decidiu segurar a bola.")

    def with_ball(self, game_state): return False
    
    def team_with_ball(self, game_state): return False
    
    def can_shoot(self, game_state): return False
    
    def can_pass(self, game_state): return False
    
    def can_dribble(self, game_state): return False
    
    def shoot(self): print("Chutei no gol!")

    def __str__(self):
        return f"Jogador: {self.name} | Posição: {self.position} | Moral: {self.moral} | Cond. Física {self.fisical_fitness} | Over: {self.calculate_overall(self.position)}"

# if __name__ == "__main__":
#     jogador1.personality.append(Personality.LEADER)
#     print(jogador1)
#     action = {
#         'with_ball': 'yes',
#         'in_goal': 'yes',
#         'derivation': 5
#     }
#     jogador1.decide_action(action)


