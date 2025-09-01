from ..models.teams import Team
from ..core.odds import simulate_pass
import random

FIXTURE_TOTAL_TIME = 90*60
TICK_TIME = .1

class MatchState:
    def __init__(self, team_home: Team, team_away: Team) -> None:
        self.team_home = team_home
        self.team_away = team_away
        self.current_time = 0
        self.home_score = 0
        self.away_score = 0
        self.ball_possession = None
        self.ball_position = (0, 0)
        self.events = []
        
    def player_team(self, player):
        if player in self.team_home.players:
            return self.team_home
        else:
            return self.team_away

class Fixture:
    def __init__(self, team_home: Team, team_away: Team) -> None:
        self.state = MatchState(team_home, team_away)
        self.boolean = 0  
        
    def tick_simulate(self):
        self.update_positions()
        
        for player in self.state.team_home.players + self.state.team_away.players:
            decided_action = player.decide_action({
                'with_ball': 'yes',
                'in_goal': 'yes',
                'derivation': 5
            })
            self.proccess_player_action(player, decided_action)
            
        # Processar todos os eventos dojogo (gols, faltas, etc.)
        self.proccess_all_events()
        
        # att tempo
        self.state.current_time += TICK_TIME
        
    def update_positions(self):
        # TODO fazer lógica
        pass
    
    def proccess_all_events(self):
        pass
    
    def proccess_player_action(self, player, action):
        if action == "shoot":
            self._simulate_shoot(player)
        elif action == "pass":
            self._simulate_pass(player)
         
    def _simulate_shoot(self, player):
        # print(f"{player.name} chutou!")
            
        # print(shooter_team.name)
        if random.random() < .1:
            shooter_team = self.state.player_team(player)
            if shooter_team == self.state.team_home:
                self.state.away_score += 1
            else:
                self.state.home_score += 1
            # print(f"GOOOOOL! Placar: {self.state.home_score}x{self.state.away_score}")
            # self.state.events.append(f"Gol de {player.name} aos {self.state.current_time:.1}s")
            
    def _simulate_pass(self, player, distance, pression, stadium_condition):
        can_pass = simulate_pass(player, 24, 12, 'wet')
        print(f"{player.name} deu um passe. Status: {can_pass}")
        
    def simulate_fixture(self):
        total_tick = 0
        while self.state.current_time < FIXTURE_TOTAL_TIME:
            total_tick+= 1
            self.tick_simulate()
            if self.state.current_time % 600 <= 0.1:
                print(f"Tempo: {self.state.current_time/60:.0f} min. Placar: {self.state.home_score} x {self.state.away_score}")
        print(f"Fim de jogo! Placar final: {self.state.home_score} x {self.state.away_score}\n{total_tick}")