import random
import numpy as np

def simulate_pass(pass_quality: int, pression: int) -> bool:
    base_success_chance = pass_quality / 20.0
    succes_chance = base_success_chance * (1 - (pression / 20.0 * .15))
    
    succes_chance = max(0, min(1, succes_chance))
    
    print(succes_chance)
    
    if random.random() < succes_chance:
        return True, "Passe certo"
    else:
        return False, "Passe errado"

def simulate_goals(media_goals: float) -> float:
    return np.random.poisson(media_goals)
    
sucesso, resultado = simulate_pass(9, 20)
# for _ in range(100):
print(f"Resultado do passe: {resultado}")

gols_time_a = simulate_goals(1.5)
gols_time_b = simulate_goals(0.8)

print("Gols do time A:", gols_time_a)
print("Gols do time B:", gols_time_b)
    
