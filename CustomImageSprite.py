import pygame


class CustomImageSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, image_name, pos, groups):
        """
        Конструктор класса CustomImageSprite.

        Создает объект спрайта с пользовательским изображением.

        Параметры:
        image_path (str): Путь к файлу изображения.
        image_name (str): Название изображения (без пути к файлу).
        pos (tuple): Кортеж с координатами (x, y) для размещения спрайта на экране.
        groups (list): Список групп спрайтов, к которым будет добавлен данный спрайт.
        """
        super().__init__(groups)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.image_name = image_name