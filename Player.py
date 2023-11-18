from Sprite import Sprite


class Player(Sprite):
    def __init__(self, color, width, height, start_pos, sprite_path):
        super().__init__(color, width, height, sprite_path)
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]