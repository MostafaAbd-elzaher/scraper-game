import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((0, 200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0
        self.gravity = 0.35

    def update(self, platforms):

        self.calc_grav()

        # --- التحقق من الاصطدامات ---

        # 1. الحركة الأفقية
        self.rect.x += self.change_x
        # التحقق من الاصطدام بعد الحركة الأفقية
        block_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # 2. الحركة الرأسية
        self.rect.y += self.change_y
        # التحقق من الاصطدام بعد الحركة الرأسية
        block_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.change_y = 0
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
                self.change_y = 0

    def calc_grav(self):
        # تزيد الجاذبية من السرعة الرأسية
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += self.gravity

    def jump(self, platforms):
        # يجب أن نتحقق إذا كان اللاعب على الأرض قبل السماح بالقفز
        # نقوم بالتحقق من وجود منصة بكسل واحد أسفل اللاعب
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2

        # إذا كانت القائمة ليست فارغة (أي أنه يلامس منصة)، اسمح له بالقفز
        if len(platform_hit_list) > 0:
            self.change_y = -10

    # باقي الدوال (go_left, go_right, stop) تبقى كما هي
    def go_left(self):
        self.change_x = -5

    def go_right(self):
        self.change_x = 5

    def stop(self):
        self.change_x = 0
