# enemy.py
import pygame
import random
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, maze, cell_size, color=(255, 0, 0)):
        super().__init__()
        
        self.maze = maze
        self.cell_size = cell_size
        self.rows = len(maze)
        self.cols = len(maze[0])
        
        # ⬅️ تحميل صورة واحدة للعدو (للاتساق)
        try:
            original_image = pygame.image.load('enemy_sprite.png').convert_alpha()
            self.image = pygame.transform.scale(original_image, (self.cell_size, self.cell_size))
        except pygame.error:
            # Fallback
            self.image = pygame.Surface([cell_size, cell_size])
            self.image.fill(color)
            
        self.rect = self.image.get_rect()
        
        self.rect.x = start_x
        self.rect.y = start_y
        
        self.base_speed_pps = 150 
        self.target_x = start_x 
        self.target_y = start_y
        
    def get_current_cell(self):
        col = round(self.rect.x / self.cell_size)
        row = round(self.rect.y / self.cell_size)
        return row, col

    def choose_new_target(self):
        current_row, current_col = self.get_current_cell()

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dr, dc in directions:
            nr, nc = current_row + dr, current_col + dc
            
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.maze[nr][nc] != 1:
                    
                    self.target_x = nc * self.cell_size
                    self.target_y = nr * self.cell_size
                    return True 
        return False
        
    def update(self, dt):
        """تحديث حركة العدو باستخدام Delta Time (dt)."""
        
        distance_this_frame = self.base_speed_pps * dt
        distance_to_target = math.sqrt((self.target_x - self.rect.x)**2 + (self.target_y - self.rect.y)**2)

        if distance_to_target < distance_this_frame:
            # وصل العدو للهدف
            self.rect.x = self.target_x
            self.rect.y = self.target_y
            self.choose_new_target() 
        else:
            # التحرك بالبكسل نحو الهدف
            
            if self.rect.x < self.target_x:
                self.rect.x += distance_this_frame
            elif self.rect.x > self.target_x:
                self.rect.x -= distance_this_frame

            if self.rect.y < self.target_y:
                self.rect.y += distance_this_frame
            elif self.rect.y > self.target_y:
                self.rect.y -= distance_this_frame