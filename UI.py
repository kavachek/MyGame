import pygame

# Интерфейс игры
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'joystix.ttf'
UI_FONT_SIZE = 18

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# Цвета_2
HEALTH_COLOR: str = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# Данные для оружия
weapon_data = {
    'нож': {'cooldown': 100, 'damage': 15, 'graphic': 'нож_полный.png'},
    'топор': {'cooldown': 100, 'damage': 25, 'graphic': 'топор_полный.png'},
}

# Данные для магии
magic_data = {
    'flame': {'strength': 5, 'cost': 30, 'graphic': 'огонь.png'},
    'heal': {'strength': 20, 'cost': 10, 'graphic': 'воздух.png'},
}


class UI:
    """
       Класс для отображения интерфейса игры.

       Этот класс управляет отображением различных элементов интерфейса, таких как
       панели здоровья и энергии, изображения оружия и магических способностей.

       Attributes:
           display_surface (pygame.Surface): Поверхность для отображения игры.
           font (pygame.font.Font): Шрифт для текстовых элементов интерфейса.
           Wingchest_bar_rect (pygame.Rect): Прямоугольник для отображения панели здоровья (кристаллы здоровья).
           Aviculture_bar_rect (pygame.Rect): Прямоугольник для отображения панели энергии (птичьи перья).
           weapon_graphics (list): Список поверхностей изображений оружия.
           magic_graphics (list): Список поверхностей изображений магических способностей.

       Methods:
           show_bar(current, max_amount, bg_rect, color):
               Отображает полосу состояния на интерфейсе.
           selection_box(left, top, has_switched):
               Отображает прямоугольник выбора элемента в интерфейсе.
           weapon_overlay(weapon_index, has_switched):
               Отображает изображение оружия на интерфейсе.
           magic_overlay(magic_index, has_switched):
               Отображает изображение магической способности на интерфейсе.
           display(player):
               Отображает интерфейс игрока, включая панели состояния, оружие и магические способности.
       """
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # настройки
        self.Wingchest_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.Aviculture_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        self.magic_graphics = []
        for magic in magic_data.values():
            magic = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        """
       Отображает полосу состояния на интерфейсе.

       Parameters:
           current (int): Текущее значение полосы состояния (здоровье или энергия).
           max_amount (int): Максимальное значение полосы состояния (здоровье или энергия).
           bg_rect (pygame.Rect): Прямоугольник, представляющий фон полосы состояния.
           color (tuple): Цвет полосы состояния.

       Метод отображает фон и полосу состояния на указанной поверхности, а также рамку вокруг нее.
        :rtype: object
       """
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def selection_box(self, left, top, has_switched):
        """
       Отображает прямоугольник выбора элемента в интерфейсе.

       Parameters:
           left (int): Координата X левого верхнего угла прямоугольника.
           top (int): Координата Y левого верхнего угла прямоугольника.
           has_switched (bool): Указывает, выбран ли элемент (True) или нет (False).

       Returns:
           pygame.Rect: Прямоугольник выбора элемента.

       Метод отображает прямоугольник с определенным цветом рамки вокруг него.
       Если элемент выбран, цвет рамки отличается от обычного.
       """
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        """
        Отображает изображение оружия на интерфейсе.

        Parameters:
            weapon_index (int): Индекс изображения оружия в списке `weapon_graphics`.
            has_switched (bool): Указывает, выбрано ли оружие (True) или нет (False).

        Метод отображает изображение оружия на интерфейсе в указанной позиции.
        Если оружие выбрано, его изображение отличается от обычного.
        """
        bg_rect = self.selection_box(30, 630, has_switched)  # оружие
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        """
        Отображает изображение магической способности на интерфейсе.

        Parameters:
            magic_index (int): Индекс изображения магической способности в списке `magic_graphics`.
            has_switched (bool): Указывает, выбрана ли магическая способность (True) или нет (False).

        Метод отображает изображение магической способности на интерфейсе в указанной позиции.
        Если магическая способность выбрана, ее изображение отличается от обычного.
        """

        bg_rect = self.selection_box(105, 635, has_switched)  # оружие
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        """
        Отображает интерфейс игрока, включая панели состояния, оружие и магические способности.

        Parameters:
            player (Player): Объект игрока, от которого берутся значения состояния и текущих выборов.

        Метод отображает все элементы интерфейса, такие как панели здоровья и энергии,
        изображения оружия и магических способностей в соответствии с текущим состоянием игрока.
        """
        self.show_bar(player.Wingchest, player.stats['Крылострудие'], self.Wingchest_bar_rect, HEALTH_COLOR)
        self.show_bar(player.Aviculture, player.stats['Птичегия'], self.Aviculture_bar_rect, ENERGY_COLOR)

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)