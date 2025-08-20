import json
import random

def load_players():
    """Carregar jogadores"""
    with open("players.json", "r") as f:
        return json.load(f)
    
def load_teams():
    """Carregar times"""
    with open("teams.json", "r") as f:
        return json.load(f)
    
all_players = load_players()
all_teams = load_teams()

def find_team_by_id(team_id: int):
    """Procurar time pelo ID"""
    return next((t for t in all_teams if t['id'] == team_id), None)

def find_players_by_team(team_id: int):
    """Procurar todos os jogadores de um time"""
    team = find_team_by_id(team_id)
    players = [p for p in all_players if p["club"] == team["nome"]]
    return players

def calc_over(player):
    weight_attack = 2
    weight_defense = 2
    weight_goalkepper = 2
    weight_fisical = 2
    weight_mental = 4
    
    habilities = [r for _, r in player["atributes"]["technique"].items()]
    fisical = [r for _, r in player["atributes"]["fisical"].items()]
    mental = [r for _, r in player["atributes"]["mental"].items()]
    
    player_attack = habilities[:10]
    player_defense = habilities[10:15]
    player_goalkepper = habilities[15:]
    
    player_attack_avarage = sum(player_attack)//len(player_attack)
    player_defense_avarage = sum(player_defense)//len(player_defense)
    player_goalkepper_avarage = sum(player_goalkepper)//len(player_goalkepper)
    fisical_avarage = sum(fisical)//len(fisical)
    mental_avarage = sum(mental)//len(mental)
    
    match player["position"]:
        case "GK":
            weight_goalkepper = 8
        case "RB" | "LB" | "LCB" | "CB" | "RCB":
            weight_defense = 8
            weight_fisical = 6
        case "LWB" | "CDM" | "RWB":
            weight_defense = 6
            weight_fisical = 4
            weight_attack = 4
        case "LM" | "LCM" | "RCM" | "RM" | "CM":
            weight_defense = 6
            weight_fisical = 4
            weight_attack = 6
        case "CAM":
            weight_defense = 4
            weight_attack = 8
        case "LW" | "RW" | "SS" | "CF" | "ST":
            weight_fisical = 6
            weight_attack = 8
            
    return ( mental_avarage*weight_mental + fisical_avarage*weight_fisical + player_attack_avarage*weight_attack + player_defense_avarage*weight_defense + player_goalkepper_avarage*weight_goalkepper )//( weight_defense+weight_attack+weight_goalkepper+weight_fisical+weight_mental )
        
def calc_team_overall(team_id: int) -> tuple[str, int]:
    """Calcular média de overall de um time"""
    team = find_team_by_id(team_id)
    players = find_players_by_team(team_id)
    over_sum = 0
    for player in players:
        over_sum += calc_over(player)
    
    over_av = over_sum // len(players)
    
    return team['nome'], over_av

def simular_partida(team_id_home, team_id_away):
    goal_home = 0
    goal_away = 0

    team_home = find_team_by_id(team_id_home)
    team_away = find_team_by_id(team_id_away)
    _, team_home_overall = calc_team_overall(team_id_home)
    _, team_away_overall = calc_team_overall(team_id_away)

    diff = abs(team_home_overall - team_away_overall)
    over_av = (team_home_overall + team_away_overall) // 2

    random_goal_chance = 150 - (diff*1.5) - (over_av*.5)

    if random_goal_chance < 1:
        random_goal_chance = 1
    
    for time in range(1, 91):
        if random.randint(1, int(random_goal_chance)) == 1:
            probability_home = team_home_overall
            probability_away = team_away_overall

            goal_choice = random.choices(
                [team_home['nome'], team_away['nome']],
                weights=[probability_home, probability_away],
                k=1
            )[0]
        
            if goal_choice == team_home['nome']:
                goal_home += 1
            else:
                goal_away += 1

    resultado = {
        "placar": {
            f"{team_home['nome']}": goal_home,
            f"{team_away['nome']}": goal_away
        }
    }

    return resultado
for i in range(50):
    resultado = simular_partida(1, 2)
    print("Placar:", resultado["placar"])

    

