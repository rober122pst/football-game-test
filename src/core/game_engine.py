from ..models.teams import Team
from ..models.players import Player, Position
from ..core.odds import simulate_pass
from .player_move import ZoneManager, CoordinatorLines
import random
import math
from typing import Tuple, List

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
        self.move_engine = SmoothMoveEngine()
        self.lines_coordinator = CoordinatorLines()
        self.zone_manager = ZoneManager()
        self.colision_system = ColisionSystem()
        
    def tick_simulate(self, state: MatchState):
        self._update_target_position(state)
        self._update_fisical_movement(state)
        # Colisões
        all_players = state.team_home.players + state.team_away.players
        self.colision_system.resolve_colisions(all_players)
        
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
        
class SmoothMoveEngine:
    def __init__(self) -> None:
        self.max_vel = {
            Position.GOALKEEPER: 3, # m/s
            Position.CENTRE_BACK: 6,
            Position.CENTRAL_ATTACK_MID: 7,
            Position.STRIKER: 8
        }
        
    def update_player_position(self, player: Player, delta_time: float):
        """Atualiza posição do jogador movendo-o suavemente em direção ao objetivo."""
        if not hasattr(player, 'target_position'):
            return
        
        current_x, current_y = player.current_pos
        target_x, target_y = player.target_position
        
        # Calcular vetor de movimento
        dx = target_x - current_x
        dy = target_y - current_y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < .1:
            return
        
        # Normalizar
        dx_norm = dx / distance
        dy_norm = dy / distance
        
        base_vel = self.max_vel.get(player.position, 6)
        
        real_vel = base_vel * (player.technique_attr['acceleration'] / 20) * (player.fisical_fitness / 100)
        
        # Calcular movimento no frame
        x_move = dx_norm * real_vel * delta_time 
        y_move = dy_norm * real_vel * delta_time
        
        # Aplicar movimento, mas não ultrapassar o objetivo
        if abs(x_move) > abs(dx):
            x_move = dx
        if abs(y_move) > abs(dy):
            y_move
            
        # Atualizar posição
        new_x = current_x + x_move 
        new_y = current_y + y_move
        
        new_x = max(-52.5, min(52.5, new_x))
        new_y = max(-34, min(34, new_y))
        
        player.current_pos = (new_x, new_y)
        
        # Atualizar fadiga baseada no movimento
        distance_traveled = math.sqrt(x_move**2 + y_move**2)
        additional_fatigue = distance_traveled * 0.1
        player.fisical_fitness = max(0, player.fisical_fitness - additional_fatigue)
        
class ColisionSystem:
    def __init__(self, player_radius: float = 0.5):
        self.player_radius = player_radius
        
    def verify_colision(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> bool:
        """Verifica se duas posições se colidem"""
        distance = math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
        return distance < (self.player_radius * 2)
    
    def resolve_colisions(self, players: List[Player]):
        """Resolve colisões entre jogadores"""
        for i, player1 in enumerate(players):
            for j, player2 in enumerate(players[i+1:], i+1):
                if self.verify_colision(player1.current_pos, player2.current_pos):
                    x1, y1 = player1.current_pos
                    x2, y2 = player2.current_pos
                    
                    dx = x1 - x2
                    dy = x2 - y2
                    distance = math.sqrt(dx**2 + dy**2)
                    
                    if distance == 0: # Mesma posição
                        dx, dy = random.uniform(-1, 1), random.uniform(-1, 1)
                        distance = math.sqrt(dx**2 + dy**2)
                        
                # Normalizar e aplicar separação
                dx_norm = dx / distance
                dy_norm = dy / distance
                
                min_separation = self.player_radius * 2.1
                move = (min_separation - distance) / 2
                
                # Mover os 2 jogadores
                player1.current_pos = (
                    x1 + dx_norm * move,
                    y1 + dy_norm * move
                )
                player2.current_pos = (
                    x2 - dx_norm * move,
                    y2 - dy_norm * move
                )