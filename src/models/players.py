from enum import Enum
from dataclasses import dataclass

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
        pass

    def decide_with_ball(self, game_state):
        """Decide a ação do jogador quando está com a bola"""
        pass

    def with_ball(self, game_state): return 

    def __str__(self):
        return f"Jogador: {self.name} | Posição: {self.position} | Moral: {self.moral} | Cond. Física {self.fisical_fitness} | Over: {self.calc_overall()}"



# jogador1.personality.append(Personality.LEADER)
# print(jogador1)


