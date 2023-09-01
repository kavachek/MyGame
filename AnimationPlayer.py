import os
import pygame
from random import choice


class AnimationPlayer:
    def __init__(self):
        """
        Конструктор класса AnimationPlayer.

        Инициализирует словарь frames, содержащий наборы изображений для различных анимаций.
        """
        self.frames = {
            'flame': self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/flame/frames'),
            'aura': self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/aura'),
            'heal': self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/heal/frames'),

            'claw': self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/claw'),
            'slash': self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/slash'),
            'sparkle': self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/sparkle'),
            'left_attack': self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/leaf_attack'),
            'thunder': self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/thunder'),

            'squid': self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/smoke_orange'),
            'raccoon': self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/raccoon'),

            'leaf': (
                self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/leaf1'),
                self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/leaf2'),
                self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/leaf3'),
                self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/leaf4'),
                self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/leaf5'),
                self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/leaf6'),
                self.reflect_images(self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/leaf1')),
                self.reflect_images(self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/leaf2')),
                self.reflect_images(self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/leaf3')),
                self.reflect_images(self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/leaf4')),
                self.reflect_images(self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/leaf5')),
                self.reflect_images(self.import_folder('C:/Users/Жена/PycharmProjects/game/graphics/particles/leaf6')),
            )
        }

    @staticmethod
    def reflect_images(frames):
        """
        Создает зеркальные копии изображений в переданном списке frames.

        Параметры:
        frames (list): Список изображений, для которых требуется создать зеркальные копии.

        Возвращает:
        list: Список зеркальных копий изображений.
        """
        new_frames = []

        if frames is not None:
            for frame in frames:
                flipped_frame = pygame.transform.flip(frame, True, False)
                new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        """
        Создает эффект частиц типа 'leaf' в указанной позиции.

        Параметры:
        pos (tuple): Кортеж с координатами (x, y) для размещения эффекта частиц.
        groups (list): Группы спрайтов, в которые добавляется объект ParticleEffect.
        """
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        """
        Создает эффект частиц указанного типа в указанной позиции.

        Параметры:
        animation_type (str): Тип анимации для эффекта частиц (например, 'flame', 'aura' и т.д.).
        pos (tuple): Кортеж с координатами (x, y) для размещения эффекта частиц.
        groups (list): Группы спрайтов, в которые добавляется объект ParticleEffect.
        """
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)

    @staticmethod
    def import_folder(folder_path):
        """
        Загружает все изображения из указанной папки folder_path.

        Параметры:
        folder_path (str): Путь к папке с изображениями.

        Возвращает:
        list: Список изображений (pygame.Surface).
        """
        frames = []

        file_names = os.listdir(folder_path)

        for file_name in file_names:
            full_path = os.path.join(folder_path, file_name)
            image_surf = pygame.image.load(full_path).convert_alpha()
            frames.append(image_surf)

        return frames
