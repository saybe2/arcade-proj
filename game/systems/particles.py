from __future__ import annotations

import math
import random
from typing import List, Tuple

import arcade


class Particle(arcade.SpriteSolidColor):
    def __init__(
        self,
        x: float,
        y: float,
        size: int,
        color: arcade.Color,
        velocity: Tuple[float, float],
        lifetime: float,
    ):
        super().__init__(size, size, color)
        self.base_color = tuple(color[:3]) if len(color) >= 3 else (255, 255, 255)
        self.color = self.base_color
        if len(color) >= 4:
            self.alpha = int(color[3])
        self.center_x = x
        self.center_y = y
        self.velocity = velocity
        self.lifetime = max(lifetime, 0.05)
        self.elapsed = 0.0

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.velocity[0] * delta_time
        self.center_y += self.velocity[1] * delta_time
        self.elapsed += delta_time
        if self.elapsed >= self.lifetime:
            self.remove_from_sprite_lists()
            return
        remaining = max(0.0, 1.0 - (self.elapsed / self.lifetime))
        self.color = (*self.base_color, int(255 * remaining))


class ParticleEmitter:
    def __init__(self):
        self.particles = arcade.SpriteList()
        self.finished = False

    def emit_burst(
        self,
        position: Tuple[float, float],
        color: arcade.Color,
        count: int = 8,
        speed_range: Tuple[float, float] = (30.0, 120.0),
        lifetime_range: Tuple[float, float] = (0.3, 0.7),
        size_range: Tuple[int, int] = (3, 6),
    ):
        x, y = position
        min_speed, max_speed = speed_range
        min_life, max_life = lifetime_range
        min_size, max_size = size_range
        for _ in range(max(1, count)):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(min_speed, max_speed)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            lifetime = random.uniform(min_life, max_life)
            size = random.randint(min_size, max_size)
            particle = Particle(x, y, size, color, velocity, lifetime)
            self.particles.append(particle)

    def update(self, delta_time: float = 1 / 60):
        self.particles.update(delta_time)
        if len(self.particles) == 0:
            self.finished = True

    def draw(self):
        self.particles.draw()


class ParticleManager:
    def __init__(self):
        self.emitters: List[ParticleEmitter] = []

    def update(self, delta_time: float):
        for emitter in list(self.emitters):
            try:
                emitter.update(delta_time)
            except TypeError:
                emitter.update()
            if getattr(emitter, "finished", False):
                self.emitters.remove(emitter)

    def draw(self):
        for emitter in self.emitters:
            emitter.draw()

    def clear(self):
        self.emitters.clear()
