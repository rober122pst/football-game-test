import pygame
import sys


class PygameInterface:
    def __init__(self):
        pygame.init()
        self.WIDTH = 1200
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Football Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.SCALE = 10
        self.FIELD_WIDTH = 105 * self.SCALE
        self.FIELD_HEIGHT = 68 * self.SCALE

        self.field_top = (self.HEIGHT - self.FIELD_HEIGHT) // 2
        self.field_bottom = self.field_top + self.FIELD_HEIGHT
        self.field_left = (self.WIDTH - self.FIELD_WIDTH) // 2
        self.field_right = self.field_left + self.FIELD_WIDTH
        self.field_middle_x = (self.field_left + self.field_right) // 2
        self.field_middle_y = (self.field_top + self.field_bottom) // 2

        self.paused = True
        self.speed = 1

    def draw_field(self):
        FIELD_COLOR = (25, 156, 77)
        WHITE = (255, 255, 255)
        line_width = 2

        self.screen.fill(FIELD_COLOR)

        # Faixas
        for i in range(0, 10, 2):
            pygame.draw.rect(self.screen, (18, 140, 75), (self.field_left + i * (self.FIELD_WIDTH // 10), self.field_top, self.FIELD_WIDTH // 10, self.FIELD_HEIGHT))

        # Linhas
        pygame.draw.rect(self.screen, WHITE, (self.field_left, self.field_top, self.FIELD_WIDTH, self.FIELD_HEIGHT), line_width)
        pygame.draw.line(self.screen, WHITE, (self.field_middle_x, self.field_top), (self.field_middle_x, self.field_bottom), line_width)
        pygame.draw.circle(self.screen, WHITE, (self.field_middle_x, self.field_middle_y), 9 * self.SCALE, line_width)
        pygame.draw.circle(self.screen, WHITE, (self.field_middle_x, self.field_middle_y), 4)

        # Áreas
        pygame.draw.circle(self.screen, WHITE, (self.field_left + 11 * self.SCALE, self.field_middle_y), 9 * self.SCALE, line_width)
        pygame.draw.rect(self.screen, FIELD_COLOR, (self.field_left, (self.HEIGHT - 40 * self.SCALE) // 2, 16.5 * self.SCALE, 40 * self.SCALE))
        pygame.draw.rect(self.screen, FIELD_COLOR, (self.field_left, (self.HEIGHT - 18 * self.SCALE) // 2, 5.5 * self.SCALE, 18 * self.SCALE))
        pygame.draw.rect(self.screen, WHITE, (self.field_left, (self.HEIGHT - 40 * self.SCALE) // 2, 16.5 * self.SCALE, 40 * self.SCALE), line_width)
        pygame.draw.rect(self.screen, WHITE, (self.field_left, (self.HEIGHT - 18 * self.SCALE) // 2, 5.5 * self.SCALE, 18 * self.SCALE), line_width)
        pygame.draw.circle(self.screen, WHITE, (self.field_left + 11 * self.SCALE, self.field_middle_y), 4)

        pygame.draw.circle(self.screen, WHITE, (self.field_right - 11 * self.SCALE, self.field_middle_y), 9 * self.SCALE, line_width)
        pygame.draw.rect(self.screen, FIELD_COLOR, (self.field_right - 16.5 * self.SCALE, (self.HEIGHT - 40 * self.SCALE) // 2, 16.5 * self.SCALE, 40 * self.SCALE))
        pygame.draw.rect(self.screen, FIELD_COLOR, (self.field_right - 5.5 * self.SCALE, (self.HEIGHT - 18 * self.SCALE) // 2, 5.5 * self.SCALE, 18 * self.SCALE))
        pygame.draw.rect(self.screen, WHITE, (self.field_right - 16.5 * self.SCALE, (self.HEIGHT - 40 * self.SCALE) // 2, 16.5 * self.SCALE, 40 * self.SCALE), line_width)
        pygame.draw.rect(self.screen, WHITE, (self.field_right - 5.5 * self.SCALE, (self.HEIGHT - 18 * self.SCALE) // 2, 5.5 * self.SCALE, 18 * self.SCALE), line_width)
        pygame.draw.circle(self.screen, WHITE, (self.field_right - 11 * self.SCALE, self.field_middle_y), 4)

        # Escanteios
        pygame.draw.circle(self.screen, WHITE, (self.field_left+1, self.field_top+1), 1 * self.SCALE, line_width)
        pygame.draw.circle(self.screen, WHITE, (self.field_left+1, self.field_bottom-1), 1 * self.SCALE, line_width)
        pygame.draw.circle(self.screen, WHITE, (self.field_right-1, self.field_top+1), 1 * self.SCALE, line_width)
        pygame.draw.circle(self.screen, WHITE, (self.field_right-1, self.field_bottom-1), 1 * self.SCALE, line_width)

        # Barras
        pygame.draw.rect(self.screen, WHITE, (self.field_left - 1 * self.SCALE, self.field_middle_y - 3.5 * self.SCALE, 1 * self.SCALE, 7 * self.SCALE))
        pygame.draw.rect(self.screen, WHITE, (self.field_right, self.field_middle_y - 3.5 * self.SCALE, 1 * self.SCALE, 7 * self.SCALE))

    def draw_players(self, match_state):
        for player in match_state.team_home.players:
            x, y = self.map_position_screen(player.positioning)
            pygame.draw.circle(self.screen, (0, 0, 255), (int(x), int(y)), 10)
        for player in match_state.team_away.players:
            x, y = self.map_position_screen(player.positioning)
            pygame.draw.circle(self.screen, (255, 0, 0), (int(x), int(y)), 10)

    def draw_ball(self, match_state):
        x, y = self.map_position_screen(match_state.ball_position)
        pygame.draw.circle(self.screen, (255, 255, 0), (int(x), int(y)), 5)    

    def draw_hud(self, match_state):
        score_text = f"{match_state.team_home.name} {match_state.home_score} x {match_state.away_score} {match_state.team_away.name}"
        score_surface = self.font.render(score_text, True, (255, 255, 255))
        self.screen.blit(score_surface, ((self.WIDTH - score_surface.get_width()) // 2, 10))

        minutes = int(match_state.current_time // 60)
        seconds = int(match_state.current_time % 60)
        timer_text = f"{minutes:02}:{seconds:02d}"
        timer_surface = self.font.render(timer_text, True, (255, 255, 255))
        self.screen.blit(timer_surface, (self.WIDTH - 100, 10))

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.type == pygame.K_r:
                    self.reset_game()
                elif event.type == pygame.K_1:
                    self.speed = .5
                elif event.type == pygame.K_2:
                    self.speed = 1
                elif event.type == pygame.K_3:
                    self.speed = 2
                elif event.type == pygame.K_4:
                    self.speed = 5
                elif event.type == pygame.K_5:
                    self.speed = 10
                elif event.type == pygame.K_ESCAPE:
                    return False
        return True

    def draw(self, match_state):
        self.draw_field()
        self.draw_players(match_state)
        self.draw_ball(match_state)
        self.draw_hud(match_state)

    def update(self, match_state):
        pass

    def execute(self, match_state):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.update(match_state)
            self.draw(match_state)

            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

    def map_position_screen(self, position: tuple) -> tuple:
        """
        Maps a position from the football field coordinate system to the screen coordinate system.

        Args:
            position (tuple): (x, y) coordinates where (0, 0) is the center of the field,
                              x ranges from -52.5 to 52.5 meters, y ranges from -34 to 34 meters.

        Returns:
            tuple: (x, y) coordinates mapped to the pygame screen.
        """
        x_ratio = (position[0] + 52.5) / 105
        y_ratio = (position[1] + 34) / 68
        x_screen = self.field_left + x_ratio * self.FIELD_WIDTH
        y_screen = self.field_top + y_ratio * self.FIELD_HEIGHT
        return (x_screen, y_screen)