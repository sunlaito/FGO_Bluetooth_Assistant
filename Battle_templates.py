from FGO_func import *


# def battle():
#     # 判断是否进入战斗界面
#     # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
#     time.sleep(8)  # 等待战斗开始
#     Current_state.WaitForBattleStart()
#     # time.sleep(6)                   #等待6秒，因为礼装效果掉落暴击星会耗时
#     # Turn1
#     character_skill(3, 1, 1)
#     character_skill(2, 1, 1)
#     character_skill(1, 1)
#     character_skill(1, 3, 1)
#     card()
#
#     # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
#     time.sleep(10)  # 等待战斗动画播放完成
#     Current_state.WaitForBattleStart()
#     # Turn2
#     character_skill(3, 3, 1)
#     Master_skill(Mystic_Codes.Chaldea_Combat_Uniform, 3, 3, 2)
#     character_skill(3, 3)
#     character_skill(3, 2)
#     card()
#
#     # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
#     time.sleep(10)  # 等待战斗动画播放完成
#     Current_state.WaitForBattleStart()
#     # Turn3
#     character_skill(3, 1, 1)
#     character_skill(2, 3, 1)
#     card()


def WCBA_GoldenEgg():
    # 判断是否进入战斗界面
    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(8)  # 等待战斗开始
    Current_state.WaitForBattleStart()
    # time.sleep(6)                   #等待6秒，因为礼装效果掉落暴击星会耗时

    # 伯爵+CBA+CBA
    # Turn1
    character_skill(3, 1, 1)
    character_skill(2, 1, 1)
    character_skill(1, 2)
    card()

    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(10)  # 等待战斗动画播放完成
    Current_state.WaitForBattleStart()
    # Turn2
    character_skill(3, 3, 1)
    card()

    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(10)  # 等待战斗动画播放完成
    Current_state.WaitForBattleStart()
    # Turn3
    Master_skill(Mystic_Codes.Template, 1, 1)
    Master_skill(Mystic_Codes.Template, 2)
    Master_skill(Mystic_Codes.Template, 3, 1)
    character_skill(2, 3, 1)
    character_skill(3, 2)
    character_skill(2, 2)
    character_skill(1, 1)
    card()


def WCBA_normal():
    # 判断是否进入战斗界面
    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(8)  # 等待战斗开始
    Current_state.WaitForBattleStart()
    # time.sleep(6)                   #等待6秒，因为礼装效果掉落暴击星会耗时

    # 伯爵+CBA+CBA
    # Turn1
    character_skill(3, 1, 1)
    character_skill(2, 1, 1)
    character_skill(1, 2)
    card()

    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(10)  # 等待战斗动画播放完成
    Current_state.WaitForBattleStart()
    # Turn2
    character_skill(3, 3, 1)
    card()

    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(10)  # 等待战斗动画播放完成
    Current_state.WaitForBattleStart()
    # Turn3
    character_skill(2, 3, 1)
    character_skill(3, 2)
    character_skill(2, 2)
    character_skill(1, 1)
    card()


def QP():
    # 判断是否进入战斗界面
    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(8)  # 等待战斗开始
    Current_state.WaitForBattleStart()
    # time.sleep(6)                   #等待6秒，因为礼装效果掉落暴击星会耗时

    # general
    # Turn1
    # character_skill(3, 3)  # 大英雄
    character_skill(3, 2)  # 斯巴达克斯
    card(3)

    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(10)  # 等待战斗动画播放完成
    Current_state.WaitForBattleStart()
    # Turn2
    card(1)

    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(10)  # 等待战斗动画播放完成
    Current_state.WaitForBattleStart()
    # Turn3
    card(2)


def GoldenEgg():
    # 判断是否进入战斗界面
    time.sleep(8)  # 等待战斗开始
    Current_state.WaitForBattleStart()

    # 尼托+狂金时+梅林
    # Turn1
    character_skill(1, 1)  # 斯巴达克斯
    card(1)

    time.sleep(10)  # 等待战斗动画播放完成
    Current_state.WaitForBattleStart()
    # Turn2
    character_skill(1, 2)
    card(1)

    time.sleep(10)  # 等待战斗动画播放完成
    Current_state.WaitForBattleStart()
    # Turn3
    character_skill(3, 1)
    character_skill(3, 3, 2)
    character_skill(2, 1)
    character_skill(2, 2)
    card(2)