import pygame
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        """
        Конструктор класса Entity.

        Параметры:
        groups (list): Группы спрайтов, в которые добавляется текущий объект.
        """
        super().__init__(groups)
        self.obstacle_sprites = None  # Группа спрайтов препятствий для обработки столкновений
        self.rect = None  # Прямоугольник, ограничивающий объект
        self.hitbox = None  # Прямоугольник-столкновение для обработки коллизий
        self.frame_index = 0  # Индекс текущего кадра анимации
        self.animation_speed = 0.15  # Скорость анимации (время между сменой кадров)
        self.direction = pygame.math.Vector2()  # Направление движения объекта

    def move(self, speed):
        """
        Метод для перемещения объекта.

        Параметры:
        speed (float): Скорость перемещения объекта.

        Примечание:
        Метод перемещает объект в указанном направлении с заданной скоростью, учитывая столкновения с препятствиями.
        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('горизонталь')
        self.hitbox.y += self.direction.y * speed
        self.collision('вертикаль')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """
        Метод для обработки столкновений объекта с препятствиями.

        Параметры:
        direction (str): Направление столкновения ('горизонталь' или 'вертикаль').

        Примечание:
        Метод проверяет столкновение объекта с препятствиями из группы препятствий и корректирует его позицию, чтобы
        избежать пересечения с препятствиями.
        """
        if direction == 'горизонталь':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'вертикаль':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    @staticmethod
    def wave_value():
        """
        Статический метод для вычисления значения волны.

        Возвращает:
        int: Значение волны от 0 до 255 в зависимости от текущего времени.

        Примечание:
        Метод использует функцию синуса для создания эффекта "волны" при задержке времени.
        """
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
