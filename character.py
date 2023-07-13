from skill import Skill
from buff import Buff
from Chloe.chloe import *

# self.skills, self.max_hp, self.max_energy, self.buff, img_path
characters_info:list[str, tuple[list[Skill], int, int, str]]=[
    ("Chloe", [Sprout_of_blue(), Sprout_of_earth()], 10, 4, "./Chloe/chloe_card.png")
]