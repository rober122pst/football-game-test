from src.models import match, players, teams
from src.core import game_engine
from src.interface import game_interface
import json

time1 = teams.Team(87, "Sport Recife", {})
time2 = teams.Team(14, "Santa Cruz", {})

with open('data/players.json', 'r') as f:
    players_data = json.load(f)

player1 = players_data[0]

jogador1 = players.Player(
    player1['id'],
    player1['name'],
    players.Position(player1['position']),
    player1['attributes']['technique'],
    player1['attributes']['fisical'],
    player1['attributes']['mental']
)
jogador2 = players.Player(2, "Caio", players.Position.L_CENTRAL_MID,
    {
        "positioning": 20,
        "finishing": 20,
        "long_shot": 20,
        "heading": 20,
        "dribbling": 20,
        "crossing": 20,
        "long_pass": 20,
        "short_pass": 20,
        "ball_control": 20,
        "curve": 20,
        "tackling": 20,
        "interceptions": 20,
        "marking": 20,
        "sliding_tackle": 20,
        "pressure": 20,
        "reflexes": 19,
        "placing": 17,
        "goalkeeping": 19
    },
    {
        "velocity": 20,
        "acceleration": 20,
        "strength": 17,
        "stamina": 16,
        "impulse": 17,
        "balance": 16
    },
    {
        "vision": 20,
        "composition": 16,
        "decision": 15,
        "lider": 12,
        "agression": 4,
        "concentration": 17,
        "composure": 17
    })

time1.add_player(jogador1)
time2.add_player(jogador2)

if __name__ == '__main__':
    print(jogador2)
    fixture = game_engine.Fixture(time1, time2)
    interface = game_interface.PygameInterface()
    interface.execute(fixture.state)

    

