import pygame


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        """
        Конструктор класса ParticleEffect.

        Создает объект спрайта для отображения анимации эффекта частицы.

        Параметры:
        pos (tuple): Кортеж с координатами (x, y) для размещения спрайта на экране.
        animation_frames (list): Список изображений для анимации эффекта.
        groups (list): Список групп спрайтов, к которым будет добавлен данный спрайт.
        """
        super().__init__(groups)
        self.sprite_type = 'Птимагия'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        """
        Метод анимации эффекта частицы.

        Обновляет текущий кадр анимации эффекта. Если анимация завершена, спрайт уничтожается.
        """
        self.frame_index += self.animation_speed
        if int(self.frame_index) >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        """
        Метод обновления спрайта.

        Вызывается каждый кадр игры для обновления состояния спрайта.
        """
        self.animate()