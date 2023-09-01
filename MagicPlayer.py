import pygame
from random import randint

# Настройки игры
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64


class MagicPlayer:
    def __init__(self, animation_player):
        """
        Конструктор класса MagicPlayer.

        Параметры:
        animation_player (AnimationPlayer): Объект класса AnimationPlayer, отвечающий за анимацию.
        """
        self.animation_player = animation_player

    def heal(self, player, strength, cost, groups):
        """
        Метод для применения магии "лечение".

        Параметры:
        player (Player): Объект класса Player, к кому применяется магия.
        strength (int): Величина лечения.
        cost (int): Стоимость применения магии в "птичегии".
        groups (list): Группы спрайтов, в которые добавляются созданные частицы анимации.

        Примечание:
        Если у игрока достаточно "птичегии" для применения магии, то игрок лечится, а анимации "ауры" и "лечения"
        создаются в указанных группах спрайтов.
        """
        if player.Aviculture >= cost:
            player.Wingchest += strength
            player.Aviculture -= cost
            if player.Wingchest >= player.stats['Крылострудие']:
                player.Wingchest = player.stats['Крылострудие']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center + pygame.math.Vector2(0, -60), groups)

    def flame(self, player, cost, groups):
        """
        Метод для применения магии "огонь".

        Параметры:
        player (Player): Объект класса Player, к кому применяется магия.
        cost (int): Стоимость применения магии в "птичегии".
        groups (list): Группы спрайтов, в которые добавляются созданные частицы анимации.

        Примечание:
        Если у игрока достаточно "птичегии" для применения магии, то создаются частицы анимации для атаки "огонь" в
        определенном направлении, зависящем от текущего положения игрока (вправо, влево, вверх или вниз).
        """
        if player.Aviculture >= cost:
            player.Aviculture -= cost
            if player.status.split('_')[0] == 'Вид_справа':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'Вид_слева':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'Вид_спереди':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)
            for i in range(1, 6):
                if direction.x:
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y1 = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y1), groups)
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y2 = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y2), groups)
