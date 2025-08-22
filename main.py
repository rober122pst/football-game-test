import json
import random
import time
import functions
from match_algorithm import simulate_match
import functions as func

if __name__ == '__main__':
    resultado = simulate_match(1, 2)
    func.narrar_jogo(resultado)
    

