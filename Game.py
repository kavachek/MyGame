import pygame
import sys

# Настройки игры
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64


class Game:
    """
        Класс для управления игрой.

        Этот класс управляет основным циклом игры и создает объект уровня, который управляет игровыми сущностями.

        Attributes:
            screen (pygame.Surface): Поверхность для отображения игры (окно игры).
            clock (pygame.time.Clock): Объект для контроля частоты кадров.

        Methods:
            run(): Запускает игровой цикл.
        """
    def __init__(self):
        """
       Инициализация класса Game.

       Метод инициализирует библиотеку Pygame, создает окно игры с указанными размерами,
       устанавливает заголовок окна и создает объект часов для контроля частоты кадров.
       Также создает объект уровня `Level`.
       """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Пернатое Пробуждение: Попугай Принц и Потерянное Орлятко')
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)