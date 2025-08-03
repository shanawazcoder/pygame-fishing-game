import pygame
import random
import math
import os


'''
Fishing Game using Pygame Developed by Shanawaz Raza
If you like this project then please follow me on Instagram @shanawaz_programmer
For more projects visit my instagram profile @shanawaz_programmer
'''

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 200)
LIGHT_BLUE = (100, 200, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)


STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2

class Hook:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.width = 10
        self.height = 20
        self.speed = 5
        self.state = "idle"  
        self.caught_fish = None
        self.line_length = 0
        
    def drop(self):
        if self.state == "idle":
            self.state = "falling"
            self.line_length = 0
            
    def update(self):
        if self.state == "falling":
            self.y += self.speed
            self.line_length += self.speed
            
            
            if self.y >= SCREEN_HEIGHT - 50:
                self.state = "rising"
                
        elif self.state == "rising":
            self.y -= self.speed
            self.line_length -= self.speed
            
            
            if self.y <= self.start_y:
                self.state = "idle"
                self.x = self.start_x
                self.y = self.start_y
                self.line_length = 0
                if self.caught_fish:
                    self.caught_fish = None
    
    def draw(self, screen):
        
        pygame.draw.line(screen, BLACK, (self.start_x, self.start_y), (self.x, self.y), 2)
        
        
        pygame.draw.rect(screen, BLACK, (self.x - self.width//2, self.y - self.height//2, self.width, self.height))
        pygame.draw.arc(screen, BLACK, (self.x - self.width//2, self.y, self.width, self.height), 0, math.pi, 2)
        
    def move(self, dx):
        if self.state == "idle":
            self.x += dx
            self.start_x += dx
            
            if self.x < 20:
                self.x = 20
                self.start_x = 20
            elif self.x > SCREEN_WIDTH - 20:
                self.x = SCREEN_WIDTH - 20
                self.start_x = SCREEN_WIDTH - 20
    
    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

class Fish:
    def __init__(self, fish_type):
        self.type = fish_type
        
        # Set fish properties based on type
        if fish_type == "small":
            self.width = 30
            self.height = 20
            self.speed = random.uniform(1.0, 2.0)
            self.score = 10
            self.color = ORANGE
        elif fish_type == "medium":
            self.width = 50
            self.height = 30
            self.speed = random.uniform(0.8, 1.5)
            self.score = 20
            self.color = GREEN
        else: 
            self.width = 70
            self.height = 40
            self.speed = random.uniform(0.5, 1.0)
            self.score = 30
            self.color = RED
            
        # Random position and direction
        self.y = random.randint(150, SCREEN_HEIGHT - 100)
        self.direction = random.choice([-1, 1])
        
        if self.direction == 1:
            self.x = -self.width
        else:
            self.x = SCREEN_WIDTH
            
        self.caught = False
        
    def update(self):
        if not self.caught:
            self.x += self.speed * self.direction
            
    def draw(self, screen):
        # Draw fish body
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw fish tail
        if self.direction == 1:
            points = [(self.x, self.y + self.height//2), 
                      (self.x - 15, self.y), 
                      (self.x - 15, self.y + self.height)]
        else:
            points = [(self.x + self.width, self.y + self.height//2), 
                      (self.x + self.width + 15, self.y), 
                      (self.x + self.width + 15, self.y + self.height)]
        pygame.draw.polygon(screen, self.color, points)
        
        # Draw fish eye
        eye_x = self.x + self.width//3 if self.direction == 1 else self.x + 2*self.width//3
        pygame.draw.circle(screen, WHITE, (int(eye_x), int(self.y + self.height//3)), 5)
        pygame.draw.circle(screen, BLACK, (int(eye_x), int(self.y + self.height//3)), 2)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        return (self.direction == 1 and self.x > SCREEN_WIDTH) or \
               (self.direction == -1 and self.x + self.width < 0)

class Bomb:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.speed = random.uniform(0.8, 1.5)
        
        # Random position and direction
        self.y = random.randint(150, SCREEN_HEIGHT - 100)
        self.direction = random.choice([-1, 1])
        
        if self.direction == 1:
            self.x = -self.width
        else:
            self.x = SCREEN_WIDTH
            
    def update(self):
        self.x += self.speed * self.direction
        
    def draw(self, screen):
        # Draw bomb body
        pygame.draw.circle(screen, BLACK, (int(self.x + self.width//2), int(self.y + self.height//2)), self.width//2)
        
        # Draw fuse
        pygame.draw.rect(screen, BLACK, (self.x + self.width//2 - 2, self.y - 10, 4, 10))
        
        # Draw spark
        pygame.draw.circle(screen, YELLOW, (int(self.x + self.width//2), int(self.y - 10)), 3)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        return (self.direction == 1 and self.x > SCREEN_WIDTH) or \
               (self.direction == -1 and self.x + self.width < 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fishing Game Developed by Shanawaz Raza")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 72)
        
        self.reset_game()
        
    def reset_game(self):
        self.state = STATE_MENU
        self.score = 0
        self.hook = Hook(SCREEN_WIDTH // 2, 50)
        self.fish_list = []
        self.bomb_list = []
        self.game_time = 60
        self.last_time = pygame.time.get_ticks()
        self.difficulty = 1
        self.fish_spawn_timer = 0
        self.bomb_spawn_timer = 0
        
    def spawn_fish(self):
        fish_type = random.choice(["small", "medium", "large"])
        self.fish_list.append(Fish(fish_type))
        
    def spawn_bomb(self):
        self.bomb_list.append(Bomb())
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = STATE_PLAYING
                        self.last_time = pygame.time.get_ticks()
                        
                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_SPACE:
                        self.hook.drop()
                        
                elif self.state == STATE_GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = STATE_MENU
                        
        return True
        
    def update(self):
        if self.state != STATE_PLAYING:
            return
            
        
        current_time = pygame.time.get_ticks()
        elapsed = (current_time - self.last_time) / 1000 
        self.last_time = current_time
        self.game_time -= elapsed
        
        if self.game_time <= 0:
            self.state = STATE_GAME_OVER
            return
            
        # Update difficulty based on score
        self.difficulty = 1 + self.score / 100
        
        # Handle input for hook movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.hook.move(-5)
        if keys[pygame.K_RIGHT]:
            self.hook.move(5)
            
        # Update hook
        self.hook.update()
        
        # Update fish
        for fish in self.fish_list[:]:
            fish.update()
            
            # Check if fish is caught
            if self.hook.state == "falling" and not fish.caught:
                if self.hook.get_rect().colliderect(fish.get_rect()):
                    fish.caught = True
                    self.hook.caught_fish = fish
                    self.hook.state = "rising"
                    self.score += fish.score
                    
            
            if fish.caught and fish == self.hook.caught_fish:
                fish.x = self.hook.x - fish.width // 2
                fish.y = self.hook.y + self.hook.height // 2
                
            
            if fish.is_off_screen() or (fish.caught and self.hook.state == "idle"):
                self.fish_list.remove(fish)
                
        # Update bombs
        for bomb in self.bomb_list[:]:
            bomb.update()
            
            
            if self.hook.get_rect().colliderect(bomb.get_rect()):
                self.state = STATE_GAME_OVER
                
            
            if bomb.is_off_screen():
                self.bomb_list.remove(bomb)
                
        
        self.fish_spawn_timer += 1
        self.bomb_spawn_timer += 1
        
        fish_spawn_rate = max(30, int(60 / self.difficulty))  
        bomb_spawn_rate = max(90, int(180 / self.difficulty)) 
        
        if self.fish_spawn_timer >= fish_spawn_rate:
            self.spawn_fish()
            self.fish_spawn_timer = 0
            
        if self.bomb_spawn_timer >= bomb_spawn_rate:
            self.spawn_bomb()
            self.bomb_spawn_timer = 0
            
    def draw_background(self):
        
        self.screen.fill(LIGHT_BLUE)
        
        
        for i in range(0, SCREEN_WIDTH, 20):
            pygame.draw.arc(self.screen, BLUE, (i, 0, 40, 40), 0, math.pi, 3)
            
       
        pygame.draw.rect(self.screen, (139, 90, 43), (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        
        for i in range(0, SCREEN_WIDTH, 100):
            height = random.randint(30, 80)
            pygame.draw.rect(self.screen, GREEN, (i, SCREEN_HEIGHT - 50 - height, 10, height))
            
    def draw(self):
        self.draw_background()
        
        if self.state == STATE_MENU:
            title_text = self.big_font.render("FISHING GAME", True, BLACK)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
            self.screen.blit(title_text, title_rect)
            
            start_text = self.font.render("Press SPACE to Start", True, BLACK)
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(start_text, start_rect)
            
            instructions = [
                "Use LEFT/RIGHT arrows to move",
                "Press DOWN or SPACE to drop hook",
                "Catch fish, avoid bombs!",
                "Game ends after 60 seconds",
                "Game Developed By Shanawaz Raza", 
                "Follow on Insta @shanawaz_programmer for Source Code"
            ]
            
            y_offset = SCREEN_HEIGHT//2 + 50
            for instruction in instructions:
                inst_text = pygame.font.SysFont(None, 24).render(instruction, True, BLACK)
                inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH//2, y_offset))
                self.screen.blit(inst_text, inst_rect)
                y_offset += 30
                
        elif self.state == STATE_PLAYING:
           
            for fish in self.fish_list:
                fish.draw(self.screen)
                
            for bomb in self.bomb_list:
                bomb.draw(self.screen)
                
            self.hook.draw(self.screen)
            
           
            score_text = self.font.render(f"Score: {self.score}", True, BLACK)
            self.screen.blit(score_text, (20, 20))
            
            timer_text = self.font.render(f"Time: {int(self.game_time)}s", True, BLACK)
            self.screen.blit(timer_text, (SCREEN_WIDTH - 150, 20))
            
        elif self.state == STATE_GAME_OVER:
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
            self.screen.blit(game_over_text, game_over_rect)
            
            score_text = self.font.render(f"Final Score: {self.score}", True, BLACK)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(score_text, score_rect)
            
            restart_text = self.font.render("Press SPACE to Return to Menu", True, BLACK)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(restart_text, restart_rect)
            
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
