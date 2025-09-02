import heapq
import math
from typing import List, Tuple, Optional

class TaticPosition:
    def __init__(self, x: float, y: float, priority: int = 0):
        self.x = x
        self.y = y
        self.priority = priority
        self.occupied = False
        self.player = None

class MoveEngine:
    def __init__(self, field_width: float = 105.0, field_height: float = 68.0):
        self.field_width, self.field_height = (field_width, field_height)
        self.tatic_positions = {}
        self._init_tatic_positions()

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
