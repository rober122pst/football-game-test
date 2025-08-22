from data_functions import find_team_by_name
import random
import time

def fixture_stats(fixture: dict) -> dict:
    
    venue = fixture['venue']
    score = fixture['score']
    events = fixture['events']
        
    stats = {
        'venue': venue,
        'stats': [
            {
                'id': find_team_by_name(team)['id'],
                'team': team,
                'team_stats': {
                    'goals': goals,
                    'shots': len([shot for shot in events if shot['team'] == team]),
                    'on_target': len([shot for shot in events if shot['team'] == team and shot['type'] == 'SHOT_ON_TARGET' or shot['type'] == 'GOAL'])
                } 
            }
            for team, goals in score.items()
        ]
    }
    
    shots_a = stats['stats'][0]['team_stats']['shots']
    shots_b = stats['stats'][1]['team_stats']['shots']
    
    possession_a = (max(.2, shots_a/(shots_a+shots_b) + random.uniform(-.1, .1)))*100
    possession_a = int(possession_a)
    possession_b = 100-possession_a
        
    stats['stats'][0]['team_stats']['possession'] = possession_a
    stats['stats'][1]['team_stats']['possession'] = possession_b
    
    return stats

def narrar_jogo(fixture: dict):
    team_home = find_team_by_name(list(fixture['score'].keys())[0])['nome']
    team_away = find_team_by_name(list(fixture['score'].keys())[1])['nome']
    
    score_home = 0
    score_away = 0
    
    print("COMEEEEÇA O JOGO!!!\n")
    for t in range(1,91):
        for event in fixture['events']:
            if event['minute'] == t:
                match event['type']:
                    case 'SHOT':
                        print(f"{event['team']} finaliza, mas bola passa longe.")
                    case 'SHOT_ON_TARGET':
                        print(f"QUAAAAAASE! {event['team']} chuta no gol do time adversário.")
                    case 'GOAL':
                        print(f"GOOOOOOOL! {event['team']} faz um golaço!")

                        if event['team'] == team_home:
                            score_home += 1
                        else:
                            score_away += 1
                        
        print(f"{t}' | {team_home} {score_home} x {score_away} {team_away}")
        print("-"*20)
        time.sleep(1)
    
    print("FIM DE JOGO!")
    print(f"Resultado Final: {team_home} {score_home} x {score_away} {team_away}")
    print("-"*20)

    stats = fixture_stats(fixture)
    print("Publico geral:", stats['venue']['public'])
    print("\nEstatísticas do Jogo:")
    for team_stats in stats['stats']:
        print(f"Time: {team_stats['team']}")
        print(f"Gols: {team_stats['team_stats']['goals']}")
        print(f"Posse de Bola: {team_stats['team_stats']['possession']}%")
        print(f"Chutes: {team_stats['team_stats']['shots']}")
        print(f"Chutes no Gol: {team_stats['team_stats']['on_target']}")
        print("-"*20)