import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        """
        Конструктор класса Weapon.

        Параметры:
        player (Player): Объект игрока, к которому привязано оружие.
        groups (list): Группы спрайтов, в которые добавляется текущий объект.
        """
        super().__init__(groups)
        self.sprite_type = 'weapon'
        self.player = player
        self.weapon_images = {
            0: ['нож_влево.png', 'нож_вправо.png', 'нож_вниз.png', 'нож_вверх.png'],
            1: ['топор_влево.png', 'топор_вправо.png', 'топор_вниз.png', 'топор_вверх.png']
        }
        self.images = [pygame.image.load(name).convert_alpha() for name in self.weapon_images[player.weapon_index]]
        self.image = self.images[self.player.weapon_image_index]
        self.rect = self.image.get_rect(center=player.rect.center)

    def update(self):
        """
        Метод для обновления состояния оружия.

        Примечание:
        Метод обновляет изображение оружия и его позицию на основе состояния и позиции игрока.
        """
        self.images = [pygame.image.load(name).convert_alpha() for name in self.weapon_images[self.player.weapon_index]]
        self.image = self.images[self.player.weapon_image_index]

        weapon_offsets = {
            'Вид_слева': (-16, -12),
            'Вид_справа': (32, -16),
            'Вид_спереди': (16, -32),
            'Вид_сзади': (0, 0),
        }

        weapon_offset_x, weapon_offset_y = weapon_offsets[self.player.status]
        self.rect = self.image.get_rect(
            center=(self.player.rect.centerx + weapon_offset_x, self.player.rect.centery + weapon_offset_y))