import random
import matplotlib.pyplot as plt
import numpy as np

# random.seed(42)
# np.random.seed(42)

def simulate_pass(player, distance: int, pression: int, stadium_condition: str) -> bool:
    prob_base = player.technique_attr["short_pass"] / 20.0

    # Passes longos mais dificeis
    prob_base *= (1 - (distance / 50.0 * .25))
    # Ajuste da pressão do adversário
    prob_base *= (1 - (pression / 20.0 * .15))
    # Ajuste pela fadiga
    prob_base *= (player.fisical_fitness / 100.0)

    if stadium_condition == "wet":
        prob_base *= .9
    elif stadium_condition == "heavy":
        prob_base *= .85
    
    prob_base = max(0, min(1, prob_base))
    return prob_base

def simulate_goals(media_goals: float) -> float:
    return np.random.poisson(media_goals)
    
def simulate_shoot_precision(shot_quality: int, derivation: int) -> int:
    real_precision = np.random.normal(shot_quality, derivation)

    return max(0, min(20, real_precision))

# jogador1 = Player(122, "Jogador 1", Position.CENTRE_BACK, {"short_pass": 20}, {"velocity": 10}, {"vision": 12})
# resultado = simulate_pass(jogador1, 40, 14, 'dry')
# print(f"Resultado do passe: {resultado}")