import json
import random
import time
import data_functions
from match_algorithm import simulate_match
import functions as func

if __name__ == '__main__':
    # resultado = simulate_match(3, 1, fixture_weight=.8)
    # func.narrar_jogo(resultado)


    jogadores = data_functions.all_players_over_by_team(3)
    print(json.dumps(jogadores, indent=4))

    

