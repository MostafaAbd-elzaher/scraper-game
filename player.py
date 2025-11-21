# player.py
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, maze):
        super().__init__()
        self.maze = maze
        self.cell_size = 25
        self.rows = len(maze)
        self.cols = len(maze[0])
        
        self.base_speed_pps = 200 
        
        # ⬅️ منطق الصور المتحركة (Directional Animation Logic)
        self.animation_frames = {}
        self.last_direction = 'down'
        self.load_directional_frames() # دالة لتحميل الصور 
        self.current_frame = 0 # مؤشر للإطار الحالي
        self.animation_speed = 0.1 # سرعة التبديل بين الإطارات (بثواني/إطار)
        self.last_update_time = 0.0 # لتتبع آخر مرة تم فيها تحديث الإطار

        # الصورة الافتراضية عند البداية
        if self.animation_frames.get(self.last_direction):
            self.image = self.animation_frames[self.last_direction][0]
        else:
            # Fallback (في حالة عدم تحميل الصور)
            self.image = pygame.Surface([self.cell_size, self.cell_size])
            self.image.fill((0, 0, 255))
        
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

    def load_directional_frames(self):
        """
        تحميل الإطارات وتخزينها في قاموس حسب الاتجاه. 
        يجب تسمية الملفات بالنمط: run_down_1.png, run_left_2.png... إلخ
        """
        directions = ['down', 'up', 'left', 'right']
        num_frames = 4 # عدد الإطارات في كل حركة
        
        for direction in directions:
            self.animation_frames[direction] = []
            
            for i in range(1, num_frames + 1):
                file_name = f'run_{direction}_{i}.png' 
                try:
                    original_img = pygame.image.load(file_name).convert_alpha()
                    scaled_img = pygame.transform.scale(original_img, (self.cell_size, self.cell_size))
                    self.animation_frames[direction].append(scaled_img)
                except pygame.error:
                    print(f"تحذير: لم يتم العثور على ملف الصورة: {file_name}. لن تعمل الرسوم المتحركة الاتجاهية.")
                    self.animation_frames = {} 
                    return 

    def animate(self, dt, is_moving):
        """
        تقوم بتحديث إطار الرسوم المتحركة بناءً على الزمن الفارق (dt) والاتجاه.
        """
        current_frames = self.animation_frames.get(self.last_direction)
        
        if not current_frames:
            return # توقف إذا لم يتم تحميل الإطارات (سيعرض المربع الافتراضي)

        if not is_moving:
            # إذا توقف اللاعب عن الحركة، نعود للإطار الأول للاتجاه الأخير
            self.image = current_frames[0]
            self.current_frame = 0
            return

        # 1. تجميع الزمن منذ آخر تحديث
        self.last_update_time += dt
        
        # 2. التحقق من تجاوز سرعة التحديث
        if self.last_update_time >= self.animation_speed:
            self.last_update_time = 0.0 # إعادة تعيين العداد
            
            # 3. الانتقال إلى الإطار التالي
            self.current_frame = (self.current_frame + 1) % len(current_frames)
            self.image = current_frames[self.current_frame]
            
        # نضمن أن الـ rect يظل متمركزاً في نفس الموضع
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


    def move(self, dx=0, dy=0, dt=0):
        """تحريك اللاعب باستخدام Delta Time (dt)."""
        if dt == 0:
            return 

        distance_moved = self.base_speed_pps * dt
        old_x = self.rect.x
        old_y = self.rect.y
        
        moving = (dx != 0 or dy != 0)
        
        # ⬅️ تحديد الاتجاه قبل الحركة
        if moving:
            # أولوية الاتجاه الأفقي للحركة القطرية (اختياري)
            if dx > 0:
                self.last_direction = 'right'
            elif dx < 0:
                self.last_direction = 'left'
            elif dy > 0:
                self.last_direction = 'down'
            elif dy < 0:
                self.last_direction = 'up'

        # 1. الحركة الفيزيائية والاصطدام (Collision and Physics)
        if moving:
            if dx != 0:
                self.rect.x += dx * distance_moved
                self._check_collision(old_x, old_y, 'x')
                
            if dy != 0:
                self.rect.y += dy * distance_moved
                self._check_collision(old_x, old_y, 'y')
        
        # 2. ⬅️ تشغيل الرسوم المتحركة في كل إطار
        self.animate(dt, is_moving=moving) 


    def _check_collision(self, old_x, old_y, axis):
        """يتحقق من الاصطدام مع الجدران (1) في المتاهة."""
        
        min_col = int(self.rect.left // self.cell_size)
        max_col = int(self.rect.right // self.cell_size)
        min_row = int(self.rect.top // self.cell_size)
        max_row = int(self.rect.bottom // self.cell_size)
        
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    if self.maze[r][c] == 1: # 1 يمثل جدار
                        
                        if axis == 'x':
                            if self.rect.x > old_x: # يتحرك يميناً
                                self.rect.right = c * self.cell_size
                            else: # يتحرك يساراً
                                self.rect.left = (c + 1) * self.cell_size
                            return
                        
                        elif axis == 'y':
                            if self.rect.y > old_y: # يتحرك لأسفل
                                self.rect.bottom = r * self.cell_size
                            else: # يتحرك لأعلى
                                self.rect.top = (r + 1) * self.cell_size
                            return