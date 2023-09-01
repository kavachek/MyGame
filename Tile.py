import pygame

# Настройки игры
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, image=None):
        """
        Конструктор класса Tile.

        Создает объект спрайта, представляющего тайл (картографический элемент) в игре.

        Параметры:
        pos (tuple): Кортеж с координатами (x, y) для размещения спрайта на экране.
        groups (list): Список групп спрайтов, к которым будет добавлен данный спрайт.
        sprite_type (str): Тип тайла, определяющий его назначение (например, 'object' для объектов на карте).
        image (pygame.Surface, optional): Изображение тайла. Если не указано, будет создана пустая поверхность.

        Примечание:
        - Для типа 'object' корректное позиционирование будет происходить выше на TILESIZE пикселей.
        """
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = image if image else pygame.Surface((TILESIZE, TILESIZE))
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)