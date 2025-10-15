# platform_sprite.py
"""Small Platform sprite used by the level.

This file replaces a previously-named local `platform.py` which shadowed the
stdlib module `platform` and caused import errors when pygame (and its
dependencies) tried to import the standard library.
"""
import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
