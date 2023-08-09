from PlayerCards.Chloe.chloe import *
from PlayerCards.Tania.tania import *
from PlayerCards.Lucifer.lucifer import *
from PlayerCards.Petra.petra import *
from PlayerCards.Gidon.gidon import *
from PlayerCards.Astin.astin import *
from EnemyCards.Knight_beginner.knight_beginner import *
from EnemyCards.Archer_beginner.archer_beginner import *
from EnemyCards.Wizard_beginner.wizard_beginner import *
from EnemyCards.Shielder.shielder import *
from EnemyCards.Crossbow_archer.crossbow_archer import *

characters_info = [
    ["Chloe", [SproutOfBlue, SproutOfEarth], SproutOfReincarnation, 20, 4, [],
     "./PlayerCards/Chloe/chloe_card.png", "#FF0000"],
    ["Tania", [StraightCut, FlameShuriken], FlameSward, 20, 5, [],
     "./PlayerCards/Tania/tania_card.png", "#FF0000"],
    ["Lucifer", [CurseArrow, ExplodeCurse], CommingApocalypse, 20, 4, [],
     "./PlayerCards/Lucifer/lucifer_card.png", "#FF0000"],
    ["Petra", [CrackOfEarth, SummonTurret], BaseCollapse, 20, 4, [BaseInstability],
     "./PlayerCards/Petra/petra_card.png", "#FF0000"],
    ["Gidon", [BloodyBlow, VengeanceEye], UnfinishedRage, 20, 4, [],
     "./PlayerCards/Gidon/gidon_card.png", "#FF0000"],
    ["Astin", [StarFall, NightSky], StarRain, 20, 5, [],
     "./PlayerCards/Astin/astin_card.png", "#FF0000"]
]

enemies_info = [
    ["기사 견습생", [Sortie, PrepareDefence], 10, [], AI_KnightBiginner,
     "./EnemyCards/Knight_beginner/knight_beginner_card.png"],
    ["궁수 견습생", [Arrow], 7, [], AI_ArcherBiginner,
     "./EnemyCards/Archer_beginner/archer_beginner_card.png"],
    ["마법사 견습생", [EnergyBall], 6, [], AI_WizardBiginner,
     "./EnemyCards/Wizard_beginner/wizard_beginner_card.png"],
    ["방패병", [ShieldOfWrath, CounterAttack], 15, [], AI_Shielder,
     "./EnemyCards/Shielder/shielder_card.png"],
    ["석궁병", [PenetrateArrow, ContinuousFiring], 10, [], AI_Crossbow,
     "./EnemyCards/Crossbow_archer/crossbow_archer_card.png"]
]

stage_list = [([(3, (3, 3)),
                (0, (3, 1)),
                (0, (3, 2)),
                (0, (3, 4)),
                (0, (3, 5)),
                (4, (4, 1)),
                (4, (4, 5)),
                (2, (5, 2)),
                (2, (5, 4))]),
              ([(0, (2, 2)),
                (0, (2, 3)),
                (0, (2, 4)),
                (0, (3, 2)),
                (4, (3, 3)),
                (0, (3, 4)),
                (0, (4, 2)),
                (0, (4, 3)),
                (0, (4, 4))])]