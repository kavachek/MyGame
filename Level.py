from csv import reader
import os
import pygame
from random import choice, randint

# Настройки игры
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64


class Level:

    def __init__(self):
        """
             Класс уровня игры.

             Этот класс представляет уровень игры, содержит элементы уровня, такие как игрок,
             препятствия, враги, атаки, магические способности и другие объекты.

             Attributes:
                 player (Player): Объект игрока на уровне.
                 display_surface (pygame.Surface): Поверхность для отображения игры.
                 visible_sprites (Camera): Камера для отображения видимых спрайтов на экране.
                 obstacle_sprites (pygame.sprite.Group): Группа препятствий для обнаружения столкновений.
                 attack_sprites (pygame.sprite.Group): Группа спрайтов атаки для обработки столкновений.
                 attackable_sprites (pygame.sprite.Group): Группа спрайтов, которых можно атаковать.
                 current_attack (Weapon): Текущая атака игрока.
                 ui (UI): Объект интерфейса уровня.
                 animation_player (AnimationPlayer): Объект управления анимациями.
                 magic_player (MagicPlayer): Объект управления магическими способностями игрока.
             Methods:
                 import_csv_layout(path): Статический метод для импорта данных уровня из CSV-файла.
                 import_images(image_names, folder_path): Статический метод для импорта изображений.
                 create_map(): Создает карту уровня и размещает на ней объекты и спрайты.
                 create_attack(): Создает атаку игрока.
                 create_magic(style, strength, cost): Создает магическую способность игрока.
                 destroy_attack(): Уничтожает текущую атаку игрока.
                 player_attack_logic(): Обрабатывает логику атаки игрока и влияние на врагов и окружение.
                 damage_player(amount, attack_type): Наносит урон игроку и обрабатывает его уязвимость.
                 remove_liza2_2(): Удаляет спрайт с изображением 'лиза2 (2).png' из группы спрайтов.
                 show_liza2_2(): Отображает спрайт с изображением 'лиза2 (2).png' на уровне.
                 show_liza2_3(): Отображает спрайт с изображением 'лиза2 (3).png' на уровне.
                 trigger_death_particles(pos, particle_type): Активирует анимацию смерти врага и создает частицы.
                 run(): Выполняет обновление и отрисовку всех спрайтов и элементов уровня.
             """

        # Поверхность для отображения игры
        self.player = None
        self.display_surface = pygame.display.get_surface()

        # Камера для отображения видимых спрайтов
        self.visible_sprites = Camera()

        # Группа препятствий для обнаружения столкновений
        self.obstacle_sprites = pygame.sprite.Group()

        # атака объектов
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Создание карты уровня
        self.create_map()

        # интерфейс
        self.ui = UI()

        self.animation_player = AnimationPlayer()

        self.magic_player = MagicPlayer(self.animation_player)

        self.change_image_time = 540000  # 9 минут

        # Координаты для смены изображения
        self.change_image_coordinates = (2873, 2709)

        # Время последней смены изображения
        self.last_image_change_time = pygame.time.get_ticks()

    @staticmethod
    def import_csv_layout(path):
        """
       Статический метод для импорта данных уровня из CSV-файла.

       Parameters:
           path (str): Путь к CSV-файлу с данными уровня.

       Returns:
           list: Список списков, представляющих данные уровня.
       """
        terrain_map = []
        with open(path) as level_map:
            layout = reader(level_map, delimiter=',')
            for row in layout:
                terrain_map.append(list(row))
            return terrain_map

    @staticmethod
    def import_images(image_names, folder_path):
        """
        Статический метод для импорта изображений.

        Parameters:
            image_names (list): Список имен изображений для импорта.
            folder_path (str): Путь к папке с изображениями.

        Returns:
            list: Список поверхностей pygame, представляющих изображения.
        """
        surface_list = []
        for name in image_names:
            image_path = os.path.join(folder_path, name)
            image_surf = pygame.image.load(image_path).convert_alpha()
            surface_list.append(image_surf)
        return surface_list

    def create_map(self):
        """
        Создает карту уровня и размещает на ней объекты и спрайты.
        """
        # Импорт данных уровня
        layouts = {
            'Граница': self.import_csv_layout('12.csv'),
            'grass': self.import_csv_layout('Grass.csv'),
            'object': self.import_csv_layout('Object.csv'),
            'entities': self.import_csv_layout('map_Entities.csv')
        }

        squid_graphics = {
            'idle_images': self.import_images(['1_монстр_idle.png', '2_монстр_idle.png', '3_монстр_idle.png',
                                               '4_монстр_idle.png'], 'graphics/monsters/squid/idle'),
            'move_images': self.import_images(['0_монстр_move.png', '1_монстр_move.png', '2_монстр_move.png',
                                               '3_монстр_move.png'], 'graphics/monsters/squid/move'),
            'idle_attack': self.import_images(['4_1.png'], 'graphics/monsters/squid/attack')
        }

        raccoon_graphics = {
            'idle_images': self.import_images(['as.png', 'as_1.png', 'as_2.png', 'as_3.png', 'as_4.png', 'as_5.png'],
                                              'graphics/monsters/raccoon/idle'),
            'move_images': self.import_images(['zx.png', 'zx_1.png', 'zx_2.png', 'zx_3.png', 'zx_4.png'],
                                              'graphics/monsters/raccoon/move'),
            'idle_attack': self.import_images(['qw.png', 'qw_1.png', 'qw_2.png', 'qw_3.png'],
                                              'graphics/monsters/raccoon/attack')

        }

        # Импорт изображений
        graphics = {
            'grass': self.import_images(['grass_1.png', 'grass_2.png', 'grass_3.png'], 'graphics/grass'),
            'object': self.import_images(['0.png', '01.png', '02.png', '03.png', '04.png', '05.png', '06.png',
                                          '07.png', '08.png', '09.png', '10.png', '11.png', '12.png', '13.png',
                                          '14.png', '15.png', '16.png', '17.png', '18.png', '19.png', '20.png'],
                                         'graphics/objects')
        }

        monster_name = None  # Инициализация переменной monster_name

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        # Создание спрайтов в зависимости от стиля
                        if style == 'Граница':
                            Tile((x, y), [self.obstacle_sprites], 'невидимость')
                        elif style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            tile = Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                'grass',
                                random_grass_image
                            )
                            tile.rect.topleft = (x, y)
                            tile.hitbox.topleft = (x, y)
                        elif style == 'object':
                            object_index = int(col)
                            if object_index < len(graphics['object']):
                                object_image = graphics['object'][object_index]

                                tile = Tile((x, y - 65),
                                            [self.visible_sprites, self.obstacle_sprites], 'object', object_image)
                                tile.rect.topleft = (x, y - 65)
                                tile.hitbox.topleft = (x, y - 65)

                        if style == 'entities':
                            if col == '394':
                                # Создание игрока
                                self.player = Player(
                                    (735, 250),
                                    (self.visible_sprites,),
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                            elif col == '392':
                                monster_name = 'raccoon'
                            else:
                                monster_name = 'squid'

                            if monster_name:
                                if monster_name == 'squid':
                                    Enemy(
                                        monster_name,
                                        (x, y),
                                        [self.visible_sprites, self.attackable_sprites],
                                        squid_graphics['idle_images'],
                                        squid_graphics['move_images'],
                                        squid_graphics['idle_attack'],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particles
                                    )
                                elif monster_name == 'raccoon':
                                    Enemy(
                                        monster_name,
                                        (x, y),
                                        [self.visible_sprites, self.attackable_sprites],
                                        raccoon_graphics['idle_images'],
                                        raccoon_graphics['move_images'],
                                        raccoon_graphics['idle_attack'],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particles
                                    )

    def create_attack(self):
        """
        Создает атаку игрока.
        """
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        """
        Создает магическую способность игрока.

        Parameters:
            style (str): Стиль магической способности ('heal' или 'flame').
            strength (int): Сила магической способности.
            cost (int): Затраты магической энергии на использование.
        """
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        """
        Уничтожает текущую атаку игрока.
        """
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        """
        Обрабатывает логику атаки игрока и влияние на врагов и окружение.
        """
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collections_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collections_sprites:
                    for target_sprite in collections_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount):
        """
       Наносит урон игроку и обрабатывает его уязвимость.

       Parameters:
   й        amount (int): Количество урона.
           attack_type (str): Тип атаки (например, 'flame', 'sword', и т. д.).
       """
        if self.player.vulnerable:
            self.player.Wingchest -= amount
            self.player.vulnerable = False
            self.player.hit_time = pygame.time.get_ticks()
            self.animation_player.create_grass_particles(self.player.rect.center, [self.visible_sprites])

    def remove_liza1(self):
        for sprite in self.visible_sprites:
            if isinstance(sprite, CustomImageSprite) and sprite.image_name == 'лиза1.png':
                if sprite.rect.topleft == self.change_image_coordinates:
                    sprite.kill()
                    self.show_liza2()  # Показываем liza2 сразу после удаления liza1
                    self.last_image_change_time = pygame.time.get_ticks()  # Обновляем время после удаления

    def remove_liza2(self):
        for sprite in self.visible_sprites:
            if isinstance(sprite, CustomImageSprite) and sprite.image_name == 'лиза2.png':
                sprite.kill()

    def show_liza1(self):
        CustomImageSprite('лиза1.png', 'лиза1.png', self.change_image_coordinates, [self.visible_sprites])

    def show_liza2(self):
        CustomImageSprite('лиза2.png', 'лиза2.png', self.change_image_coordinates, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        """
       Активирует анимацию смерти врага и создает частицы.

       Parameters:
           pos (tuple): Координаты позиции анимации.
           particle_type (str): Тип частиц (например, 'grass', 'fire', и т. д.).
       """
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_image_change_time >= self.change_image_time:
            self.remove_liza1()
            self.show_liza2()
            self.last_image_change_time = current_time