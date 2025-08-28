from enum import Enum
from dataclasses import dataclass
from ..core.decision_tree import DecisionNode
import src.core.odds as odds

class PlayerState(Enum):
    ATTACKING = "Atacando"
    DEFENDING = "Defendendo"
    MARKING = "Marcando"
    WITH_POSSESSION = "Com a posse"
    WITHOUT_POSSESSION = "Sem a posse"
    LOOKING_FOR_POSITION = "Procurando posição"

class Position(Enum):
    GOALKEPPER = "GO"
    CENTRE_BACK = "ZAG"
    L_BACK = "LE"
    R_BACK = "LD"
    L_WING_BACK = "AE"
    R_WING_BACK = "AD"
    
    CENTRAL_DEFENSE_MID = "VOL"
    CENTRAL_MIDFIELDER = "MC"
    L_CENTRAL_MID = "MCE"
    R_CENTRAL_MID = "MCD"
    L_MIDFILDER = "MCE"
    CENTRAL_ATTACK_MID = "MAT"
    
    LEFT_WINGER = "PTE"
    RIGHT_WINGER = "PTD"
    SECOND_STRIKER = "SA"
    CENTRE_FOWARD = "ATA"
    STRIKER = "CA"

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
            
    def calc_overall(self) -> int:
        """Calcular overall do jogador baseado em seus atributos"""
        # TODO: fazer baseado em posição com média ponderada
        sum_attr = (self.technique_attr["short_pass"] + self.technique_attr['finishing'] + self.technique_attr['dribbling'] + self.fisical_attr['velocity'] + self.fisical_attr['strength'] + self.fisical_attr['stamina'] + self.mental_attr['vision'] + self.mental_attr['decision']) // 8
        return (sum_attr*99)//20
    
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
                    DecisionNode(value='yes', action=lambda a: odds.simulate_shoot_precision(self.technique_attr['finishing'], a['derivation'])),
                    DecisionNode(value='no', filhos=[
                        DecisionNode('friend_free', filhos=[
                            DecisionNode(value='yes', action=lambda a: odds.simulate_pass(self.technique_attr['short_pass'], a['distance'], a['pression'], a['stadium_codition'])),
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
        return f"Jogador: {self.name} | Posição: {self.position} | Moral: {self.moral} | Cond. Física {self.fisical_fitness} | Over: {self.calc_overall()}"


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

if __name__ == "__main__":
    jogador1.personality.append(Personality.LEADER)
    print(jogador1)
    action = {
        'with_ball': 'yes',
        'in_goal': 'yes',
        'derivation': 5
    }
    jogador1.decide_action(action)


