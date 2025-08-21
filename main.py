import json
import random
import time
from match_algorithm import simulate_match



# def simular_partida(team_id_home, team_id_away):
#     goal_home = 0
#     goal_away = 0

    

#     diff = abs(team_home_overall - team_away_overall)
#     over_av = (team_home_overall + team_away_overall) // 2

#     random_goal_chance = 150 - (diff*1.5) - (over_av*.5)

#     if random_goal_chance < 1:
#         random_goal_chance = 1
    
#     for time in range(1, 91):
#         if random.randint(1, int(random_goal_chance)) == 1:
#             probability_home = team_home_overall
#             probability_away = team_away_overall

#             goal_choice = random.choices(
#                 [team_home['nome'], team_away['nome']],
#                 weights=[probability_home, probability_away],
#                 k=1
#             )[0]
        
#             if goal_choice == team_home['nome']:
#                 goal_home += 1
#             else:
#                 goal_away += 1

#     resultado = {
#         "placar": {
#             f"{team_home['nome']}": goal_home,
#             f"{team_away['nome']}": goal_away
#         }
#     }

#     return resultado

if __name__ == '__main__':
    resultado = simulate_match(1, 2)
    print(resultado)
    

