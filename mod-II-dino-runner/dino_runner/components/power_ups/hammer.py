
from dino_runner.components.power_ups.power_up  import Power_Up
from dino_runner.utils.constants import  HAMMER_TYPE


class Hammer(Power_Up):
    def __init__(self, image):
        super().__init__(image)
        self.type = HAMMER_TYPE
    