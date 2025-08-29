from src.models import match, players, teams
from src.core import game_engine

time1 = teams.Team(87, "Sport Recife", {})
time2 = teams.Team(14, "Santa Cruz", {})

jogador1 = players.Player(1, "Rober", players.Position.STRIKER,
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
jogador2 = players.Player(2, "Caio", players.Position.STRIKER,
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

time1.add_player(jogador1)
time2.add_player(jogador2)

if __name__ == '__main__':
    print(f"{time1.name} vs {time2.name}")
    game_engine.Fixture(time1, time2).simulate_fixture()

    

