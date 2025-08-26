from enum import Enum

class Personality(Enum):
    LEADER = "Líder"
    INDIVIDUALIST = "Individualista"
    UNSTABLE = "Instável"
    COLD_IN_FINALS = "Frio em Finais"
    GOAL_SCORER = "Artilheiro"

class Player():
    """Classe do jogador. Todos os seus dados e atributos + funções extras"""
    def __init__(self, _id, name, position, fisical_attr, technique_attr, mental_attr):
        self.id = _id
        self.name = name
        # self.shirt_name = shirt_name
        # self.nationality = nationality
        # self.birth = birth
        # self.height = height
        # self.weight = weight
        # self.shirt_number = shirt_number
        self.position = position
        # self.foot = foot
        self.fisical_attr = fisical_attr
        self.technique_attr = technique_attr
        self.mental_attr = mental_attr
        # self.team = team

        self.moral = 50 # 0 a 100
        self.fisical_fitness = 100 # 0 a 100
        self.injury = 5 # 0 a 100
        self.experience = 0
        self.personality = []

    def __post_init__(self):
        self.technique_attr = {
            "positioning": 0,
            "finishing": 0,
            "long_shot": 0,
            "heading": 0,
            "dribbling": 0,
            "crossing": 0,
            "long_pass": 0,
            "short_pass": 0,
            "ball_control": 0,
            "curve": 0,
            "tackling": 0,
            "interceptions": 0,
            "marking": 0,
            "sliding_tackle": 0,
            "pressure": 0,
            "reflexes": 0,
            "placing": 0,
            "goalkeeping": 0
        }

        self.fisical_attr = {
            "velocity": 0,
            "acceleration": 0,
            "strength": 0,
            "stamina": 0,
            "impulse": 0,
            "balance": 0
        }

        self.mental_attr = {
            "vision": 0,
            "composition": 0,
            "decision": 0,
            "lider": 0,
            "agression": 0,
            "concentration": 0,
            "composure": 0
        }

        all_attr = self.technique_attr
        all_attr.update(self.fisical_attr)
        all_attr.update(self.mental_attr)

        print(all_attr)

    def __str__(self):
        return f"Jogador: {self.name} | Posição: {self.position} | Moral: {self.moral} | Cond. Física {self.fisical_fitness}"


    # @property
    # def short_pass(self):
    #     return self.technique_attr['short_pass']
    
    # @short_pass.setter
    # def short_pass(self, value):
    #     if 0 <= value <= 20:
    #         self.technique_attr['short_pass'] = value
    #     else:
    #         raise ValueError("O valor deve estar entre 0 e 20")


jogador1 = Player(1, "Rober", "ATA",
        {
            "positioning": 80,
            "finishing": 10,
            "long_shot": 12,
            "heading": 25,
            "dribbling": 30,
            "crossing": 20,
            "long_pass": 68,
            "short_pass": 60,
            "ball_control": 50,
            "curve": 10,
            "tackling": 20,
            "interceptions": 30,
            "marking": 35,
            "sliding_tackle": 18,
            "pressure": 50,
            "reflexes": 88,
            "placing": 82,
            "goalkeeping": 90
        },
        {
            "velocity": 40,
            "acceleration": 38,
            "strength": 82,
            "stamina": 70,
            "impulse": 85,
            "balance": 72
        },
        {
            "vision": 48,
            "composition": 72,
            "decision": 78,
            "lider": 75,
            "agression": 45,
            "concentration": 88,
            "composure": 80
        })
jogador1.personality.append(Personality.LEADER.value)
print(jogador1)


