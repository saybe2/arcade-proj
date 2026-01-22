class ParticleManager:
    def __init__(self):
        self.emitters = []

    def update(self, delta_time: float):
        for emitter in self.emitters:
            emitter.update()

    def draw(self):
        for emitter in self.emitters:
            emitter.draw()

    def clear(self):
        self.emitters.clear()
