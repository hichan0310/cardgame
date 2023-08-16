from PlayerCards.Chloe.chloe import *
from PlayerCards.Tania.tania import *
from PlayerCards.Lucifer.lucifer import *
from PlayerCards.Petra.petra import *
from PlayerCards.Gideon.gideon import *
from PlayerCards.Astin.astin import *
from EnemyCards.Knight_beginner.knight_beginner import *
from EnemyCards.Archer_beginner.archer_beginner import *
from EnemyCards.Wizard_beginner.wizard_beginner import *
from EnemyCards.Shielder.shielder import *
from EnemyCards.Crossbow_archer.crossbow_archer import *

characters_info = [
    ["Tania", [StraightCut, FlameShuriken], FlameSward, 20, 5, [],
     "./PlayerCards/Tania/tania_card.png", "#FF0000"],
    ["Lucifer", [CurseArrow, ExplodeCurse], CommingApocalypse, 20, 4, [],
     "./PlayerCards/Lucifer/lucifer_card.png", "#FF0000"],
    ["Gideon", [BloodyBlow, VengeanceEye], UnfinishedRage, 20, 4, [],
     "./PlayerCards/Gideon/gideon_card.png", "#FF0000"],
    ["Astin", [StarFall, NightSky], StarRain, 20, 5, [],
     "./PlayerCards/Astin/astin_card.png", "#FF0000"],
    ["Chloe", [SproutOfBlue, SproutOfEarth], SproutOfReincarnation, 20, 4, [],
     "./PlayerCards/Chloe/chloe_card.png", "#FF0000"],
    ["Petra", [CrackOfEarth, SummonTurret], BaseCollapse, 20, 4, [BaseInstability],
     "./PlayerCards/Petra/petra_card.png", "#FF0000"],
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

TAG_ACTIVE = "active"
TAG_COST = "cost"

EVENT_Sniping = "저격"
EVENT_HealingLight = "회복의 빛"
EVENT_EnergyRecharge = "에너지 재충전"
EVENT_Lucky = "행운"
EVENT_WarpGate = "워프 게이트"
EVENT_EnforceHit = "강화 타격"
EVENT_SecondOpportunity = "두 번째 기회"
EVENT_BombThrowing = "폭탄 투척"
EVENT_ManaSynthesizer = "마나 합성기"
EVENT_FireSward = "불타오르는 칼날"
event_card_info = {
    EVENT_Sniping: (
        EVENT_Sniping, 3,
        "./EventCards/Sniping/sniping_card.png",
        ["적군 1명을 선택하여 관통 피해를 가하고 hp를 1로 만든다.",
         "최대 7의 피해를 가한다. "],
        EVENT_TYPE_1,
    ),
    EVENT_HealingLight: (
        EVENT_HealingLight, 1,
        "./EventCards/HealingLight/healing_light.png",
        ["아군 1명을 지정하여 hp를 2 회복한다. "],
        EVENT_TYPE_1
    ),
    EVENT_EnergyRecharge: (
        EVENT_EnergyRecharge, 1,
        "./EventCards/EnergyRecharge/energy_recharge.png",
        ["아군 1명을 지정하여 필살기 게이지를 1 충전한다. "],
        EVENT_TYPE_1
    ),
    EVENT_Lucky: (
        EVENT_Lucky, 2,
        "./EventCards/Lucky/lucky.png",
        ["아군 1명을 골라서 이번 턴의 공격을 50%의 확률로 회피하는 버프를 부여한다. ",
         "관통 공격은 피할 수 없다. "],
        EVENT_TYPE_1
    ),
    EVENT_WarpGate: (
        EVENT_WarpGate, 1,
        "./EventCards/WarpGate/warp_gate.png",
        ["워프 게이트를 열어서 2개 칸을 서로 바꾼다. ",
         "이것은 이동으로 간주하지 않는다. "],
        EVENT_TYPE_2
    ),
    EVENT_EnforceHit: (
        EVENT_EnforceHit, 3,
        "./EventCards/EnforceHit/enforce_hit.png",
        ["아군 1명을 지정하여 강화 타격 버프를 부여한다. ",
         "강화 타격 상태의 적은 3턴간 일반 공격 피해가 50% 증가하는 버프를 부여한다. ",
         "소수점 아래는 버린다 . "],
        EVENT_TYPE_1
    ),
    EVENT_SecondOpportunity: (
        EVENT_SecondOpportunity, 2,
        "./EventCards/SecondOpportunity/second_opportunity.png",
        ["이번 턴 행동 가능 횟수가 1회 증가한다. "],
        EVENT_TYPE_0
    ),
    EVENT_BombThrowing: (
        EVENT_BombThrowing, 2,
        "./EventCards/BombThrowing/bomb_throwing.png",
        ["공격하면 터지면서 3의 광역 피해를 주는 폭탄을 소환한다. ",
         "폭탄은 1변 공격하면 바로 터진다. ",
         "빈 공간이 없으면 사용할 수 없다. "],
        EVENT_TYPE_1
    ),
    EVENT_ManaSynthesizer: (
        EVENT_ManaSynthesizer, 1,
        "./EventCards/ManaSynthesizer/mana_synthesizer.png",
        ["아군 1명을 골라 피해를 3번 받으면 다음 턴에 3cost를 회복하는 버프를 부여한다. "],
        EVENT_TYPE_1
    ),
    EVENT_FireSward: (
        EVENT_FireSward, 2,
        "./EventCards/FireSward/fire_sward.png",
        ["캐릭터에게 과열 상태를 부여한다. ",
         "과열 상태이 캐릭터는 스킬로 데미지를 3번 가할 때마다 cost와 필살기를 1 회복한다. ",
         "이 버프는 턴이 지나도 사라지지 않으며 중첩될 수 없다. "],
        EVENT_TYPE_1
    ),
}
