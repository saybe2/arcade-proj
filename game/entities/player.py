import arcade
from pathlib import Path
import enum


class FaceDirection(enum.Enum):
    """Направление взгляда персонажа"""
    LEFT = 0
    RIGHT = 1


class Player(arcade.Sprite):
    def __init__(self, x: float = 100, y: float = 150, scale: float = 0.1):
        super().__init__()
        
        # Основные характеристики
        self.scale = scale
        self.speed = 300
        self.health = 100
        
        # Загрузить спрайты анимации ходьбы
        self.walking_textures = []
        walking_path = Path("assets/player/anim/walking")
        
        # Загрузить кадры анимации (0.png, 1.png, ..., 8.png)
        if walking_path.exists():
            for i in range(9):  # 9 кадров (0-8)
                frame_path = walking_path / f"{i}.png"
                if frame_path.exists():
                    self.walking_textures.append(arcade.load_texture(str(frame_path)))
        
        # Если спрайты загружены - использовать первый кадр как idle
        if self.walking_textures:
            self.idle_texture = self.walking_textures[0]
            self.texture = self.idle_texture
        else:
            self.idle_texture = arcade.make_soft_square_texture(32, arcade.color.BLUE, 255, 0)
            self.texture = self.idle_texture
        
        # Параметры анимации
        self.current_frame = 0
        self.frame_counter = 0.0
        self.frame_duration = 0.1  # Длительность каждого кадра в секундах
        
        # Состояние движения
        self.is_walking = False  # Никуда не идём
        self.face_direction = FaceDirection.RIGHT  # Смотрим вправо
        
        # Позиция
        self.center_x = x
        self.center_y = y
        self.is_alive = True

    def update_animation(self, delta_time: float = 1 / 60):
        """Обновить анимацию ходьбы или покоя"""
        if self.is_walking and self.walking_textures:
            # Анимация ходьбы
            self.frame_counter += delta_time
            
            if self.frame_counter >= self.frame_duration:
                self.frame_counter = 0.0
                self.current_frame = (self.current_frame + 1) % len(self.walking_textures)
                
                # Поворачиваем текстуру в зависимости от направления взгляда
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walking_textures[self.current_frame]
                else:
                    self.texture = self.walking_textures[self.current_frame].flip_horizontally()
        else:
            # Если не идём, показываем текстуру покоя
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.idle_texture
            else:
                self.texture = self.idle_texture.flip_horizontally()
    
    def update(self, delta_time: float, keys_pressed: set):
        """Обновить движение персонажа"""
        # Определяем направление движения
        dx, dy = 0, 0
        
        if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
            dx -= self.speed * delta_time
        if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
            dx += self.speed * delta_time
        if arcade.key.UP in keys_pressed or arcade.key.W in keys_pressed:
            dy += self.speed * delta_time
        if arcade.key.DOWN in keys_pressed or arcade.key.S in keys_pressed:
            dy -= self.speed * delta_time
        
        # Нормализация диагонального движения
        if dx != 0 and dy != 0:
            factor = 0.7071  # 1/sqrt(2)
            dx *= factor
            dy *= factor
        
        # Изменяем позицию
        self.center_x += dx
        self.center_y += dy
        
        # Поворачиваем персонажа в зависимости от направления движения
        if dx < 0:
            self.face_direction = FaceDirection.LEFT
        elif dx > 0:
            self.face_direction = FaceDirection.RIGHT
        
        # Проверка на движение
        self.is_walking = (dx != 0) or (dy != 0)
