from ..models.teams import Team
from ..models.players import Player
from ..types.types import Position
from ..core.odds import simulate_pass
from .player_move import ZoneManager, CoordinatorLines, MovementBehavior
import random
import math
from typing import Tuple, List
from ..models.match import MatchState

FIXTURE_TOTAL_TIME = 90*60
TICK_TIME = .1

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

        for player in all_players:
            self.zone_manager.update_zones(player)

        for player in all_players:
            action = player.decide_action(state, state.player_team(player).coach_instructions)
            self.proccess_player_action(player, action, state)
        
        self.proccess_all_events(state)

        # att tempo
        self.state.current_time += TICK_TIME
        
    def update_positions(self):
        # TODO fazer lógica
        pass
    
    def proccess_all_events(self, state: MatchState):
        pass
    
    def proccess_player_action(self, player, action, state: MatchState):
        if action == "shoot":
            self._simulate_shoot(player)
        elif action == "pass":
            self._simulate_pass(player)
         
    def _update_target_position(self, state: MatchState):
        """Calcula onde cada jogador deveria estar posicionado."""

        def_line_home = self.lines_coordinator.calculate_defensive_line(state.team_home, state)
        def_line_away = self.lines_coordinator.calculate_defensive_line(state.team_away, state)

        for player in state.team_home.players:
            if player.position == Position.CENTRE_BACK:
                target_pos = MovementBehavior.calculate_defense_move(player, state)
            elif player.position == Position.CENTRAL_ATTACK_MID:
                target_pos = MovementBehavior.calculate_central_move(player, state)
            elif player.position == Position.STRIKER:
                target_pos = MovementBehavior.calculate_attack_move(player, state)
            elif player.position == Position.GOALKEEPER:
                target_pos = player.positioning
            player.target_position = target_pos

        for player in state.team_away.players:
            if player.position == Position.CENTRE_BACK:
                target_pos = MovementBehavior.calculate_defense_move(player, state)
            elif player.position == Position.CENTRAL_ATTACK_MID:
                target_pos = MovementBehavior.calculate_central_move(player, state)
            elif player.position == Position.STRIKER:
                target_pos = MovementBehavior.calculate_attack_move(player, state)
            elif player.position == Position.GOALKEEPER:
                target_pos = player.positioning
            player.target_position = target_pos
        
    def _update_fisical_movement(self, state: MatchState):
        """Atualiza as posições físicas dos jogadores"""
        for player in state.team_home.players + state.team_away.players:
            self.move_engine.update_player_position(player, TICK_TIME)

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

class MovementOptimizer:
    def __init__(self):
        self.calc_cache = {}
        self.last_update_cache = 0

    def _calc_movement_optimized(self, player: Player, state: MatchState):
        """
        Versão otimizada que usa cache para cálculos pesados.
        """
        # Usar cache para cálculos que não mudam a cada tick
        cache_key = f"{player._id}_{int(state.current_time // 1.0)}"

        if cache_key in self.calc_cache:
            return self.calc_cache[cache_key]
        
        result = self._calc_complet_movement(player, state) # TODO implementar

        self.calc_cache[cache_key] = result

        if state.current_time - self.last_update_cache > 10:
            self._clear_old_cache(state.current_time)
            self.last_update_cache = state.current_time

        return result
