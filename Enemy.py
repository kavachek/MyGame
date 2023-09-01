import pygame

# Данные для монстров
monster_data = {
    'squid': {'health': 50, 'exp': 100, 'damage': 20, 'attack_type': 'slash', 'attack_sound': 'slash.wav',
              'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'health': 3000, 'exp': 100, 'damage': 80, 'attack_type': 'slash', 'attack_sound': 'slash.wav',
                'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
}


class Enemy(Entity):
    def __init__(self, monster, pos, groups, idle_images, move_images, idle_attack, obstacle_sprites, damage_player,
                 trigger_death_particles):
        """
        Конструктор класса Enemy.

        Параметры:
        monster (str): Название монстра.
        pos (tuple): Позиция монстра на экране (координаты x, y).
        groups (list): Группы спрайтов, в которые добавляется текущий объект.
        idle_images (list): Список изображений для анимации покоя монстра.
        move_images (list): Список изображений для анимации движения монстра.
        idle_attack (list): Список изображений для анимации атаки монстра.
        obstacle_sprites (pygame.sprite.Group): Группа спрайтов препятствий для обработки столкновений.
        damage_player (function): Функция для нанесения урона игроку.
        trigger_death_particles (function): Функция для создания эффектов при смерти монстра.
        """
        super().__init__(groups)
        self.direction = None
        self.animations = {'idle': [], 'move': [], 'attack': []}
        self.sprite_type = 'enemy'

        self.animations['idle'] = idle_images
        self.animations['move'] = move_images
        self.animations['attack'] = idle_attack

        self.monster_name = monster
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown_duration = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        self.status = 'idle'
        self.frame_index = 0
        if self.animations.get(self.status):
            self.image = self.animations[self.status][self.frame_index]
        else:
            self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

    def get_player_distance_direction(self, player):
        """
        Метод для определения направления и расстояния до игрока.

        Параметры:
        player (Player): Объект игрока.

        Возвращает:
        tuple: Расстояние до игрока, вектор направления к игроку.

        Примечание:
        Метод вычисляет расстояние до игрока и возвращает единичный вектор направления к нему.
        """
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def get_status(self, player):
        """
        Метод для определения статуса монстра (покой, движение, атака).

        Параметры:
        player (Player): Объект игрока.

        Примечание:
        Метод определяет статус монстра на основе его расстояния до игрока и устанавливает соответствующий статус.
        """
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        """
        Метод для определения действий монстра в зависимости от его статуса.

        Параметры:
        player (Player): Объект игрока.

        Примечание:
        Метод определяет действия монстра в зависимости от его статуса (покой, движение, атака).
        """
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)

        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]

        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        """
        Метод для анимации монстра.

        Примечание:
        Метод обновляет изображение монстра в соответствии с текущим статусом и кадром анимации.
        """
        animation = self.animations[self.status]

        if not animation:
            return

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def attack_cooldowns(self):
        """
        Метод для обработки перезарядки атаки монстра.

        Примечание:
        Метод проверяет перезарядку атаки монстра и устанавливает соответствующее состояние.
        """
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown_duration:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        """
        Метод для обработки получения урона монстром.

        Параметры:
        player (Player): Объект игрока.
        attack_type (str): Тип атаки (оружие или магия).

        Примечание:
        Метод обрабатывает получение урона монстром и устанавливает состояние уязвимости.
        """
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        """
        Метод для проверки смерти монстра.

        Примечание:
        Метод проверяет, если у монстра закончилось здоровье, уничтожает его и создает эффекты при смерти.
        """
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)

    def hit_reaction(self):
        """
        Метод для реакции монстра на получение урона.

        Примечание:
        Метод меняет направление движения монстра при получении урона.
        """
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        """
        Метод для обновления состояния монстра.

        Примечание:
        Метод обновляет состояние монстра, перемещает его, анимирует и обрабатывает перезарядку атаки и смерть.
        """
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.attack_cooldowns()
        self.check_death()

    def enemy_update(self, player):
        """
        Метод для обновления монстра на основе состояния игрока.

        Параметры:
        player (Player): Объект игрока.

        Примечание:
        Метод обновляет состояние монстра на основе состояния и расстояния до игрока.
        """
        self.get_status(player)
        self.actions(player)