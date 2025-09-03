import heapq
import math
from typing import List, Tuple, Optional
from ..models.players import Player, Position
from ..models.teams import Team
from .game_engine import MatchState
import random

class TaticalPosition:
    def __init__(self, x: float, y: float, priority: int = 0):
        self.x = x
        self.y = y
        self.priority = priority
        self.occupied = False
        self.player = None

class MoveEngine:
    def __init__(self, field_width: float = 105.0, field_height: float = 68.0):
        self.field_width, self.field_height = (field_width, field_height)
        self.tatical_positions = {}
        self._init_tatical_positions()

    def pathfinder_a(self, origin: Tuple[float, float], destiny: Tuple[float, float], obstacles: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """
        Implementa A* modificado para o futebol.
        Considera:
        - Distância
        - Proximidade dos adversários
        - Zonas de perigo
        - Preferências táticas
        """

        def heuristic(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
            return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
        
        def cost(current_pos: Tuple[float, float], neighbor_pos: Tuple[float, float], obstacles: List[Tuple[float, float]]) -> float:
            base_cost = heuristic(current_pos, neighbor_pos)

            # Penalidade por proximidade de adversário
            for obstacle in obstacles:
                dist_to_obstacle = heuristic(neighbor_pos, obstacle)
                if dist_to_obstacle < 3.0: # Zona de perigo de 3 metros
                    base_cost += (3.0 - dist_to_obstacle) * 2.0

            return base_cost
        
        priority_queue = [(0, origin)]
        cost = {origin: 0}
        came_from = {origin: None}

        while priority_queue:
            current_cost, current_pos = heapq.heappop(priority_queue)

            if self._is_close(current_pos, destiny, tolerancy=1.0):
                path = []
                while current_pos is not None:
                    path.append(current_pos)
                    current_pos = came_from[current_pos]
                return path[::-1]
            
            # Explorar vizinhos (8 direções)
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
                new_pos = (current_pos[0] + dx, current_pos[1] + dy)

                # Limites do campo
                if not self._valide_pos(new_pos):
                    continue

                new_cost = cost[current_pos] + cost(current_pos, new_pos, obstacles)

                if new_pos not in cost or new_cost < cost[new_pos]:
                    cost[new_pos] = new_cost
                    priority = new_cost + heuristic(new_pos, destiny)
                    heapq.heappush(priority_queue, (priority, new_pos))
                    came_from[new_pos] = current_pos

        return [origin, destiny] # Caminho direto se falhar

class MovementBehavior:
    @staticmethod
    def calculate_defense_move(player: Player, match_state: MatchState) -> Tuple[float, float]:
        """
        Zagueiros priorizam:
        1. Manter linha defensiva
        2. Cobrir atacantes adversários
        3. Acompanha atancantes
        """
        base_position = player.positioning

        if match_state.team_with_ball != match_state.player_team(player):
            # Encontrar atacante adversário mais próximo
            closest_attacker = MoveEngine._find_closest_opponent(player, match_state) # TODO implementar
            if closest_attacker:
                # Posicionar entre o atacante e o gol
                x_goal = -52.5 if match_state.player_team(player) == match_state.team_home else 52.5

                x_attacker, y_attacker = closest_attacker.positioning

                x_ideal = (x_attacker + x_goal) / 2
                y_ideal = y_attacker

                final_x = (base_position[0] * 0.3) + (x_ideal * 0.7)
                final_y = (base_position[1] * 0.3) + (y_ideal * 0.7)

                return (final_x, final_y)
        return base_position          

    @staticmethod
    def calculate_central_move(player: Player, match_state: MatchState) -> Tuple[float, float]:
        """
        Meio-campistas são os mais dinâmicos:
        1. Oferecer opções de passe quando o time tem a bola
        2. Pressionar o portador da bola quando o adversário tem posse
        3. Manter equilíbrio entre ataque e defesa
        """
        base_position = player.positioning

        if match_state.team_with_ball == match_state.player_team(player):
            # Time tem a bola - buscar espaços para receber passe
            player_with_ball = match_state.player_with_ball

            if player_with_ball != player:
                # Calcular posição para receber passe
                x_ball, y_ball = player_with_ball.positioning
                ideal_distance = 15.0 # metros
                angle = math.atan2(base_position[1] - y_ball, base_position[0] - x_ball)

                ideal_x = x_ball + ideal_distance * math.cos(angle)
                ideal_y = y_ball + ideal_distance * math.cos(angle)

                # Verificar se tá livre
                if MoveEngine._free_position((ideal_x, ideal_y), match_state, security_radius=5.0):
                    return (ideal_x, ideal_y)
        else:
            # Time sem a bola - pressionar ou cobrir
            player_with_ball = match_state.player_with_ball
            x_ball, y_ball = player_with_ball.positioning

            pression_distance = 3.0 # metros
            angle = math.atan2(y_ball - base_position[1], x_ball - base_position[0])

            x_pression = x_ball - pression_distance * math.cos(angle)
            y_pression = y_ball - pression_distance * math.cos(angle)

            return (x_pression, y_pression)
        
        return base_position
    
    @staticmethod
    def calculate_attack_move(player: Player, match_state: MatchState) -> Tuple[float, float]:
        """
        Atacantes focam em:
        1. Buscar posições de finalização
        2. Criar espaços para companheiros
        3. Pressionar zagueiros adversários
        """
        base_position = player.positioning

        if match_state.team_with_ball == match_state.player_team(player):
            # Buscar posição de ataque
            x_opponent_goal = 52.5 if match_state.player_team(player) == match_state.team_home else -52.5

            offside_line = MoveEngine._calculate_offside_line(player, match_state) # TODO implementar

            x_ideal = min(x_opponent_goal - 5.0, offside_line - 1)
            y_ideal = base_position[1] + random.uniform(-10, 10) # Variação lateral

            return (x_ideal, max(-30, min(30, y_ideal)))
        else:
            # Pressionar zagueiros adversários
            closest_defender = MoveEngine._find_closest_opponent(player, match_state) # TODO implementar
            if closest_defender:
                x_defender, y_defender = closest_defender.positioning
                return (x_defender + 2, y_defender) # Ficar mais próximo para pressionar
            
        return base_position
    
class InfluenceZone:
    def __init__(self, center: Tuple[float, float], radius: float, intensity: float):
        self.center = center
        self.radius = radius
        self.intensity = intensity # 0 a 1

    def affects(self, position: Tuple[float, float]) -> bool:
        dist = math.sqrt(
            (position[0] - self.center[0])**2 +
            (position[1] - self.center[1])**2
        )

        if dist < self.radius:
            # Influência decai com a distância
            normalized_influence = 1 - (dist / self.radius)
            return normalized_influence * self.intensity
        return 0
    
class ZoneManager:
    def __init__(self):
        self.zones_per_player = {}

    def update_zones(self, player: Player):
        """Atualiza a zona de influência do jogador baseado em sua posição e função"""
        base_radius = { # TODO fazer com todas as pos
            Position.GOALKEEPER: 15,
            Position.CENTRE_BACK: 12,
            Position.CENTRAL_ATTACK_MID: 10,
            Position.STRIKER: 8
        }

        radius = base_radius.get(player.position, 10)
        intensity = player.position / 100
        
        self.zones_per_player[player._id] = InfluenceZone(player.current_pos, radius, intensity)
        
    def calculate_conflict_zones(self, position: Tuple[float, float], team: Team):
        """
        Calcula o nível de conflito de zonas em uma posição.
        Retorna valor entre 0 (sem conflito) e 1 (conflito máximo)
        """
        total_influence = 0
        
        for player in team.players:
            if player._id in self.zones_per_player:
                zone = self.zones_per_player[player._id]
                total_influence += zone.calculate_influence(position) # TODO implementar
                
        return min(1, total_influence)
    
class CoordinatorLines:
    def __init__(self):
        self.defensive_lines = {}
        self.ofensive_lines = {}
        
    def calculate_defensive_line(self, team: Team, match_state: MatchState):
        """Calcula posição X da linha defensiva baseada na posição dos zagueiros."""
        defensors = [j for j in team.players if j.position == Position.CENTRE_BACK]
        
        if not defensors: return 20 # posição padrão
        
        most_avanced_x = max(z.current_pos[0] for z in defensors)
        
        if match_state.team_with_ball == team:
            # Time tem a bola - linha pode subir
            most_avanced_x = min(most_avanced_x + 5, 45)
        else:
            # Linha recua quando o adversário está com a bola
            most_avanced_x = max(most_avanced_x - 3, 15)
            
        return most_avanced_x
    
    def ajust_positions_for_line(self, team: Team, defensive_line: float):
        """Ajusta as posições dos jogadores para manter a linha defensiva."""
        for player in team.players:
            if player.position == Position.CENTRE_BACK:
                current_x, current_y = player.current_pos
                # Ajustar X para manter a linha, presevar Y
                player.target_position = (defensive_line, current_y) # TODO implementar
            elif player.position == Position.CENTRAL_ATTACK_MID:
                # Meio campistas ficam 10-15 metros a frente da linha
                
                current_x, current_y = player.current_pos
                ideal_x = defensive_line + 12
                player.target_position = (ideal_x, current_y)
                
class ColetiveMovements:
    @staticmethod
    def exec_cordenate_pressing(team: Team, match_state: MatchState):
        """Implementa pressing coordenado - todos os jogadores próximos pressionam de uma vez"""
        player_with_ball = match_state.player_with_ball
        
        if not player_with_ball or match_state.player_team(player_with_ball) == team:
            return # Não precisa pressionar se o proprio time tem a bola
        
        x_ball, y_ball = player_with_ball.current_pos
        
        # Encontrar jogadores próximos à bola (raio de 15m)
        neighbor_players = []
        for player in team.players:
            distance = math.sqrt(
                (player.current_pos[0] - x_ball)**2 +
                (player.current_pos[1] - y_ball)**2
            )
            if distance <= 15: # Metros
                neighbor_players.append(player)
                
        # Coordenar movimento de pressão
        for player in neighbor_players:
            # Calcular posição de pressão (próximo a bola, mas não todos no mesmo lugar).
            base_angle = math.atan2(y_ball - player.current_pos[1], x_ball - player.current_pos[0])
            
            # Adicionar variação para não sobrepor
            angular_variation = random.uniform(-.3, .3)
            final_angle = base_angle + angular_variation
            
            pressing_distance = 2 # Metros
            x_pressing = x_ball - pressing_distance * math.cos(final_angle)
            y_pressing = y_ball - pressing_distance * math.sin(final_angle)
            
            player.target_position = (x_pressing, y_pressing)
            player.move_mode = "pressing" # TODO implementar
            
    @staticmethod
    def exec_base_transangulation(player_with_ball: Player, team: Team):
        """Cria triângulos de passe - dois jogadores se posicionam para formar opções de passe em ângulos diferentes. Movimento clássico do futebol."""
        x_ball, y_ball = player_with_ball.current_pos
        
        # Encontrar 2 companheiros próximos
        teammates = [j for j in team.players if j != player_with_ball]
        teammates.sort(key=lambda j: math.sqrt(
            (j.current_pos[0] - x_ball)**2 +
            (j.current_pos[1] - y_ball)**2
        ))
        
        if len(teammates) >= 2:
            # Primeiro companheiro - posição de apoio próxima
            teammate1 = teammates[0]
            angle1 = math.pi / 4 # 45 graus
            distance1 = 8
            x1 = x_ball + distance1 * math.cos(angle1)
            y1 = y_ball + distance1 * math.cos(angle1)
            teammate1.target_position = (x1, y1)
            
            # Segundo companheiro - posição de apoio distante
            teammate2 = teammates[1]
            angle2 = -math.pi / 4 # -45 graus
            distance2 = 12
            x2 = x_ball + distance2 * math.cos(angle2)
            y2 = y_ball + distance2 * math.cos(angle2)
            teammate2.target_position = (x2, y2)