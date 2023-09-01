import pygame

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


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        """
        Конструктор класса Player.

        Создает объект игрового персонажа, управляемого игроком.

        Параметры:
        pos (tuple): Кортеж с координатами (x, y) для размещения персонажа на экране.
        groups (list): Список групп спрайтов, к которым будет добавлен персонаж.
        obstacle_sprites (list): Список спрайтов, представляющих препятствия на карте.
        create_attack (function): Функция для создания атаки персонажа.
        destroy_attack (function): Функция для удаления атаки персонажа.
        create_magic (function): Функция для создания магии персонажа.
        """
        super().__init__(groups)
        self.hit_time = None
        self.animations = None
        self.image = pygame.image.load('яшулька_2версия.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.import_player_assets()
        self.status = 'Вид_спереди'
        self.speed = 5

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites
        self.is_attacking = False

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.weapon_image_index = 7
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # сведения об игроке и его жизнях
        self.stats = {'Крылострудие': 100, 'Птичегия': 60, 'Птичатака': 10, 'Птимагия': 4, 'Птичстрек': 5}
        # Крылострудие - здоровье, Птичегия - энергия, Птичатака - атака, Птимагия - магия, Птичстрек - скорость
        self.Wingchest = self.stats['Крылострудие'] * 0.5
        self.Aviculture = self.stats['Птичегия'] * 0.8
        self.exp = 123
        self.Ptichstrek = self.stats['Птичстрек']

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def import_player_assets(self):
        """
        Импортирует анимации и изображения для игрового персонажа.
        """
        character_path = ''  # Путь к папке с анимациями персонажа
        self.animations = {
            'Вид_сзади': ['вид_сзади1.png', 'вид_сзади2.png'],
            'Вид_слева': ['вид_слева1.png', 'вид_слева2.png'],
            'Вид_спереди': ['вид_спереди1.png', 'вид_спереди2.png'],
            'Вид_справа': ['вид_справа1.png', 'вид_справа2.png']
        }

        for animation_key in self.animations:
            animation_files = self.animations[animation_key]
            animation_images = []
            for file in animation_files:
                full_path = character_path + file
                image_surf = pygame.image.load(full_path).convert_alpha()
                animation_images.append(image_surf)
            self.animations[animation_key] = animation_images

    def input(self):
        """
        Обработка пользовательского ввода.

        Реагирует на нажатия клавиш для управления персонажем, а также для атаки и магии.
        """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        # Атака
        if keys[pygame.K_e] and not self.attacking:
            self.attacking = True
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()

        # Магия
        if keys[pygame.K_q] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            style = list(magic_data.keys())[self.magic_index]
            strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['Птимагия']
            cost = list(magic_data.values())[self.magic_index]['cost']

            self.create_magic(style, strength, cost)

        if keys[pygame.K_r] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()

            if self.weapon_index < len(list(weapon_data.keys())) - 1:
                self.weapon_index += 1
            else:
                self.weapon_index = 0

            self.weapon = list(weapon_data.keys())[self.weapon_index]

        if keys[pygame.K_TAB] and self.can_switch_magic:
            self.can_switch_magic = False
            self.magic_switch_time = pygame.time.get_ticks()

            if self.magic_index < len(list(magic_data.keys())) - 1:
                self.magic_index += 1
            else:
                self.magic_index = 0

            self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        """
        Получает текущее направление персонажа и обновляет его статус.

        Используется для определения текущего направления персонажа и установки соответствующего статуса.
        """
        if self.direction.x == 0 and self.direction.y == 0:
            if self.is_attacking:
                var = self.status
            return

        if self.direction.y < 0:
            self.status = 'Вид_сзади'
            self.weapon_image_index = 3
        elif self.direction.y > 0:
            self.status = 'Вид_спереди'
            self.weapon_image_index = 2
        elif self.direction.x < 0:
            self.status = 'Вид_слева'
            self.weapon_image_index = 0
        elif self.direction.x > 0:
            self.status = 'Вид_справа'
            self.weapon_image_index = 1

    def damage_player(self, amount):
        """
        Наносит урон персонажу.

        Параметры:
        amount (int): Количество урона, которое наносится персонажу.
        attack_type (str): Тип атаки, определяющий тип урона (например, 'weapon' или 'magic').
        """
        if self.vulnerable:
            self.Wingchest -= amount
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    def cooldowns(self):
        """
        Обработка перезарядки.

        Контролирует перезарядку атаки, смены оружия и магии, а также времени неуязвимости после получения урона.
        """
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        """
        Анимация персонажа.

        Обновляет анимацию персонажа в зависимости от его текущего статуса и направления.
        """
        animation = self.animations[self.status]

        if self.direction.magnitude() != 0:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        """
        Получает полный урон от оружия.

        Возвращает значение, равное базовому урону от атаки персонажа плюс урон от текущего оружия.
        """
        base_damage = self.stats['Птичатака']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        """
        Получает полный урон от магии.

        Возвращает значение, равное базовому урону от магии плюс урон от текущего заклинания.
        """
        base_damage = self.stats['Птимагия']
        spell_damage = magic_data.get(self.Aviculture, {}).get('strength', 0)
        return base_damage + spell_damage

    def Aviculture_recovery(self):
        """
        Восстановление Птичегии (энергии).

        Восстанавливает энергию персонажа (Птичегию) на 0.01 * Птимагия, если ее текущее значение меньше максимального.
        """
        if self.Aviculture < self.stats['Птичегия']:
            self.Aviculture += 0.01 * self.stats['Птимагия']
        else:
            self.Aviculture = self.stats['Птичегия']

    def update(self):
        """
        Обновление персонажа.

        Выполняет обработку пользовательского ввода, контроль перезарядки и анимацию,
         а также обновляет позицию персонажа.
        """
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.Aviculture_recovery()