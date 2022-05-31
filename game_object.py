import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    """ Этот класс описывает управление и поведение спрайта игрока"""
    
    # Конструктор класса player
    def __init__(self, x, y, img='fish.png'):
        super().__init__()
        # Загружаем изображение спрайта
        self.image = pygame.image.load(img).convert_alpha()
        # Задаем начальное положение спрайта игрока на экране
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        # Задаем начальную скорость игрока по x и по y
        self.change_x = 0
        self.change_y = 0
        self.platforms = pygame.sprite.Group()
        self.artifacts = pygame.sprite.Group()
        #артифакты и жизни в начале игры
        self.score = 0
        self.lives = 5


    def update(self):
        # учитываем эффект гравитации:
        self.calc_grav()
        # Пересчитываем положение спрайта игрока на экране

        # Смещение влево - вправо
        self.rect.x += self.change_x

        # Проверяем столкновение с препятствием по горизонтали
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            # Если персонаж двигался вправо, остановим его слева от препятствия
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Наоборот, если движение было влево остановим его справа от препятствия
                self.rect.left = block.rect.right

        # Движение вверх-вниз
        self.rect.y += self.change_y

        # Проверяем столкновение с препятствием по верикали
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            # При движении вниз, персонаж упал на препятвие - он должен встать на него сверху
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                #Если персонаж двигался вверх, остановим его снизу от препятствия
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # В прыжке персонаж врезался в препятствия - движение вверх должно прекратиться.
            self.change_y = 0

        # Проверяем столкновение с артефактом
        artifact_hit_list = pygame.sprite.spritecollide(self, self.artifacts, False)
        for artifact in artifact_hit_list:
            self.score += 1
            artifact.kill()

    # Расчет гравитации
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            # Моделируем ускорение свободного падения:
            self.change_y += 0.35

        # Проверка: персонаж на земле или нет
        if self.rect.y >= WIN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = WIN_HEIGHT - self.rect.height

        # Проверка: выход за левую границу экрана
        if self.rect.x < 0 :
            self.rect.x = 0
            self.change_x = 0
        

    # Движения контролируемые игроком:
    def jump(self):
        """ Вызывается при нажатии стрелки вверх """

        # Опускаемся на 2 пикселя вниз, чтобы проверить наличие платформы под игроком
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 2

        # проверяем можно ли прыгать
        if len(platform_hit_list) > 0 or self.rect.bottom >= WIN_HEIGHT:
            self.change_y = -10
            
    def go_left(self):
        """ Вызывается при нажатии стрелки влево """
        self.change_x = -6

    def go_right(self):
        """ Вызывается при нажатии стрелки вправо """
        self.change_x = 6

    def stop(self):
        """ Вызывается когда игрок отпускает клавишу """
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, type, color=BLUE,img='ground00.png'):
        super().__init__()
        # Загружаем изображение спрайта
        self.image = pygame.image.load(img).convert_alpha()
        # Помещаем прямоугольник в заданное место на экране
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Artifact(pygame.sprite.Sprite):
    def __init__(self, x, y, img='coin.png'):
        super().__init__()
        # Задаем размеры прямоугольника
        self.image = pygame.image.load(img).convert_alpha()
        # Задаем положение спрайта на экране
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

# Класс Enemy описывает противника персонажа
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, img='jellyfish.png'):
        super().__init__()
        # Загружаем изображение в спрайт
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # спрайт противника ходит туда - обратно по горизонтали от точки start до точки stop:
        self.start = x
        self.stop = x
        # направление перемещения противника 1 - вправо, -1 - влево
        self.direction = 1
        # скосроть перемещения противника
        self.speed = speed
    
    # Обрабатываем сдвиг противника при сдвиге мира
    def shift(self, x):
        self.rect.x += x
        self.start += x
        self.stop += x

    def update(self):
        # спрайт дошел то stop и должен повернуть обратно, налево
        if self.rect.x >= self.stop:
            self.rect.x = self.stop
            self.direction = -1
        # спрайт дошел до start и должен повернуть обратно, направо
        if self.rect.x <= self.start:
            self.rect.x = self.start
            self.direction = 1
        # смещаем спрайт в указанном направлении
        self.rect.x += self.direction * self.speed



