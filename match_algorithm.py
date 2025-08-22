import random
import math
from typing import List, Dict, Any
import data_functions as data_f

def _poisson_sample(lam: float) -> int:
    # algoritmo de Knuth para Poisson
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while True:
        k += 1
        p *= random.random()
        if p <= L:
            return k - 1

def simulate_match(team_id_a: float, team_id_b: float, fixture_weight: float = 1.0, minutes: int = 90, seed: int | None = None) -> Dict[str, Any]:
    """
    Simula uma partida minuto-a-minuto baseada no overall dos times.
    Retorna dicionário com placar final e lista de eventos.
    over_a, over_b: valores de 0 a 100 (overall)
    """
    if seed is not None:
        random.seed(seed)
        
    name_a, over_a = data_f.calc_team_overall(team_id_a)
    name_b, over_b = data_f.calc_team_overall(team_id_b)

    # Parâmetros ajustáveis (brinque com eles)
    base_chances_per_match = 15.0   # expectativa total de chances (soma dos dois times)
    gamma = 2                     # sensibilidade: >1 aumenta diferença entre over altos e baixos
    conversion_base = 0.10          # probabilidade base de um chance virar gol (antes de modifiers)
    diff_total_boost = 1.8          # quanto o total de chances sobe com diferença grande (opcional)

    # normalizar / preparar pesos
    weight_a = (max(0.0, over_a) ** gamma)
    weight_b = (max(0.0, over_b) ** gamma)

    # diferença normalizada -1..1
    diff_norm = (over_a - over_b) / 100.0
    # ajustar total de chances por minuto levemente com base na diferença absoluta
    mu_total_per_min = (base_chances_per_match / minutes) * (1.0 + abs(diff_norm) * diff_total_boost)

    events: List[Dict[str, Any]] = []
    score_a = 0
    score_b = 0

    # momentum simples: aumenta conversão por curto período após gol
    momentum_a = 0.0
    momentum_b = 0.0
    momentum_decay = 0.6  # multiplicador por minuto

    for minute in range(1, minutes + 1):
        # recalcula probabilidades relativas (pode manter fixo, mas deixei recalculável)
        total_weight = weight_a + weight_b
        prob_a = weight_a / total_weight if total_weight > 0 else 0.5

        # número de chances esse minuto (Poisson)
        n_chances = _poisson_sample(mu_total_per_min)

        for _ in range(n_chances):
            # decide qual time criou a chance
            if random.random() < prob_a:
                team = name_a
                team_over = over_a
                momentum = momentum_a
            else:
                team = name_b
                team_over = over_b
                momentum = momentum_b

            # probabilidade de ser gol: base * (overall/100) * ruido * (1 + momentum)
            ruido = random.uniform(0.6, 1.4)  # variação natural do futebol
            prob_goal = conversion_base * (team_over / 100.0) * ruido * (1.0 + 0.25 * momentum)
            # garante prob_goal entre 0 e (quase) 1
            prob_goal = max(0.0, min(prob_goal, 0.95))

            if random.random() < prob_goal:
                if team == name_a:
                    score_a += 1
                    momentum_a = 1.0 
                    events.append({"minute": minute, "team": name_a, "type": "GOAL"})
                else:
                    score_b += 1
                    momentum_b = 1.0
                    events.append({"minute": minute, "team": name_b, "type": "GOAL"})
            elif ruido > 1.1:
                events.append({"minute": minute, "team": team, "type": "SHOT_ON_TARGET"})
            else:
                events.append({"minute": minute, "team": team, "type": "SHOT"})

        # decay de momentum
        momentum_a *= momentum_decay
        momentum_b *= momentum_decay

    return {
        "venue": simulate_public(team_id_a, fixture_weight),
        "score": {name_a: score_a, name_b: score_b},
        "events": events
    }

def simulate_public(team_id, fixture_weight):
    team = data_f.find_team_by_id(team_id)
    estadio = team["estadio"]
    capacidade = estadio["capacidade"]
    taxa = estadio["taxa_ocupacao_media"]
    
    ocupacao = max(.2, min(1, taxa * fixture_weight))
    ocupacao = max(.2, min(1, ocupacao * (1+random.uniform(-.1, .1))))
    
    public = capacidade * ocupacao
    
    return {
        "name": estadio['nome'],
        "public": int(public)
    }
    