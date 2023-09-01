import pygame


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # Поверхность для отображения игры
        self.display_surface = pygame.display.get_surface()

        # Половина ширины и высоты поверхности отображения
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        # Смещение камеры относительно игрока
        self.offset = pygame.math.Vector2(300, 200)

        # Инициализация поверхности для отрисовки фона
        self.floor_surf = pygame.image.load('карта.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

        """
        Класс для управления камерой в игре.

        Этот класс управляет смещением камеры относительно игрового мира и отображает игровые объекты
        с учетом смещения, чтобы сосредоточить камеру на игроке.

        Attributes:
            display_surface (pygame.Surface): Поверхность для отображения игры.
            half_width (int): Половина ширины поверхности отображения игры.
            half_height (int): Половина высоты поверхности отображения игры.
            offset (pygame.math.Vector2): Вектор смещения камеры относительно игрока.
            floor_surf (pygame.Surface): Поверхность для отображения фона уровня.
            floor_rect (pygame.Rect): Прямоугольник, представляющий фоновую поверхность.

        Methods:
            custom_draw(player): Отображает игровые объекты с учетом смещения камеры.
            enemy_update(player): Обновляет положение вражеских спрайтов с учетом положения игрока.
        """

    def custom_draw(self, player):

        # Вычисление смещения камеры относительно игрока
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Отображение фона
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # Отображение спрайтов с учетом смещения камеры
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_post = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_post)

    """
    Отображает игровые объекты с учетом смещения камеры.

    Parameters:
        player (Player): Объект игрока, относительно которого смещается камера.

    Метод отображает фоновую поверхность уровня и игровые спрайты с учетом смещения камеры
    относительно игрока, чтобы сосредоточить камеру на нем.
    """

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and
                         sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

    """
    Обновляет положение вражеских спрайтов с учетом положения игрока.

    Parameters:
        player (Player): Объект игрока, используется для вычисления положения вражеских спрайтов.

    Метод вызывает метод `enemy_update()` для каждого вражеского спрайта,
    чтобы обновить их положение относительно игрока.
    """