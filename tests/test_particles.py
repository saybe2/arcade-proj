from game.systems.particles import ParticleManager


class DummyEmitter:
    def __init__(self):
        self.update_calls = 0
        self.draw_calls = 0

    def update(self):
        self.update_calls += 1

    def draw(self):
        self.draw_calls += 1


def test_particle_manager_update_and_draw():
    manager = ParticleManager()
    emitter = DummyEmitter()
    manager.emitters.append(emitter)

    manager.update(1 / 60)
    manager.draw()

    assert emitter.update_calls == 1
    assert emitter.draw_calls == 1


def test_particle_manager_clear():
    manager = ParticleManager()
    manager.emitters.append(DummyEmitter())
    manager.clear()
    assert manager.emitters == []
