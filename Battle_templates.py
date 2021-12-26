from FGO_func import *


def WCBA_GoldenEgg():
    # 判断是否进入战斗界面
    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(8)  # 等待战斗开始

    # 伯爵+CBA+CBA
    # Turn1
    Current_state.WaitForBattleStart()
    character_skill(3, 1, 1)
    character_skill(2, 1, 1)
    character_skill(1, 2)
    card()

    # Turn2
    Current_state.WaitForBattleStart()
    character_skill(3, 3, 1)
    card()

    # Turn3
    Current_state.WaitForBattleStart()
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

    # 伯爵+CBA+CBA
    # Turn1
    Current_state.WaitForBattleStart()
    character_skill(3, 1, 1)
    character_skill(2, 1, 1)
    character_skill(1, 2)
    card()

    # Turn2
    Current_state.WaitForBattleStart()
    character_skill(3, 3, 1, check=True)  # CBA给伯爵充能, 关键
    card()

    # Turn3
    Current_state.WaitForBattleStart()
    character_skill(2, 3, 1, check=True)  # CBA给伯爵充能, 关键
    character_skill(3, 2)
    character_skill(2, 2)
    character_skill(1, 1)
    card()


def QP():
    # 判断是否进入战斗界面
    # Serial.mouse_set_zero()         #鼠标复位,防止误差累积
    time.sleep(8)  # 等待战斗开始

    # 宝具+宝具+(自充&宝具)
    # Turn1
    Current_state.WaitForBattleStart()
    # character_skill(3, 3, check=True)  # 大英雄
    character_skill(3, 2, check=True)  # 斯巴达克斯自充, 关键技能
    card(3)

    # Turn2
    Current_state.WaitForBattleStart()
    card(1)

    # Turn3
    Current_state.WaitForBattleStart()
    card(2)


def GoldenEgg():
    # 判断是否进入战斗界面
    time.sleep(8)  # 等待战斗开始

    # 尼托+狂金时+梅林
    # Turn1
    Current_state.WaitForBattleStart()
    character_skill(1, 1)
    card(1)

    # Turn2
    Current_state.WaitForBattleStart()
    character_skill(1, 2, check=True)  # 尼托自充, 关键技能
    card(1)

    # Turn3
    Current_state.WaitForBattleStart()
    character_skill(2, 2, check=True)  # 金时自充, 关键技能
    character_skill(2, 1)
    character_skill(3, 1)
    character_skill(3, 3, 2)
    card(2)


def WCaber_normal():
    time.sleep(8)  # 等待战斗开始

    # mainC+Caber+Caber
    # Turn1
    Current_state.WaitForBattleStart()
    character_skill(2, 1, check=True)
    character_skill(2, 2, 1, check=True)
    character_skill(2, 3, 1, check=True)
    character_skill(3, 1, check=True)
    character_skill(3, 2, 1, check=True)
    character_skill(3, 3, 1, check=True)

    character_skill(1, 1, check=True)
    card()

    # Turn2
    Current_state.WaitForBattleStart()
    card()

    # Turn3
    Current_state.WaitForBattleStart()
    card()


def WCaber_lin():
    time.sleep(8)  # 等待战斗开始

    # Lin(with 60start energy)+Caber+Caber
    # Turn1
    Current_state.WaitForBattleStart()

    character_skill(2, 1, check=True)
    character_skill(2, 2, 1, check=True)
    character_skill(2, 3, 1, check=True)

    character_skill(3, 2, 1, check=True)
    character_skill(3, 3, 1, check=True)

    character_skill(1, 1)
    card()

    # Turn2
    Current_state.WaitForBattleStart()
    character_skill(3, 1, check=True)

    card()

    # Turn3
    Current_state.WaitForBattleStart()
    character_skill(1, 3)

    card()


def infPool21():
    time.sleep(8)  # 等待战斗开始

    # 美狄亚+剑呆+C呆+孔明
    # Turn1
    print("T1")
    Current_state.WaitForBattleStart()
    character_skill(3, 3, 1, check=True)
    character_skill(2, 1)
    character_skill(1, 1, check=True)
    card(1)

    # Turn2
    print("T2")
    Current_state.WaitForBattleStart()
    character_skill(2, 1, check=True)
    character_skill(2, 3)
    # C呆换孔明
    while True:
        Master_skill(Mystic_Codes.Chaldea_Combat_Uniform, 3, 3, 1)
        time.sleep(1)
        Serial.touch(1000, 170, 4)  # 战斗菜单
        Serial.touch(1000, 100, 5)  # 御主头像
        Flag, Position = Base_func.match_template('KMFlag')
        if Flag:
            break
    Current_state.WaitForBattleStart()
    character_skill(3, 3, check=True)
    character_skill(3, 2, check=True)
    character_skill(3, 1, 1, check=True)
    card(1)

    # Turn3
    print("T3")
    Current_state.WaitForBattleStart()
    character_skill(2, 2)
    character_skill(2, 3, check=True)
    Master_skill(Mystic_Codes.Chaldea_Combat_Uniform, 1)
    card(2)


def ymt21():
    time.sleep(8)  # 等待战斗开始

    # 宇宙凛+剑阿荣+C呆
    # Turn1
    print("T1")
    Current_state.WaitForBattleStart()
    character_skill(1, 1)
    character_skill(3, 1, check=True)
    character_skill(3, 2, 1, check=True)
    character_skill(3, 3, 1, check=True)
    card(1)

    # Turn2
    print("T2")
    Current_state.WaitForBattleStart()
    character_skill(2, 1, check=True)
    character_skill(2, 3)
    # C呆换C呆
    while True:
        Master_skill(Mystic_Codes.Chaldea_Combat_Uniform, 3, 3, 1)  # 前排3换后排1
        time.sleep(3)
        Serial.touch(1000, 170, 4)  # 战斗菜单
        Serial.touch(1000, 100, 5)  # 御主头像
        Flag, Position = Base_func.match_template('CBFlag')
        if Flag:
            break
    Current_state.WaitForBattleStart()
    character_skill(3, 1, check=True)
    character_skill(3, 2, 2, check=True)
    # character_skill(3, 3, 2)
    card(2)

    # Turn3
    print("T3")
    Current_state.WaitForBattleStart()
    character_skill(1, 3, check=True)
    # character_skill(1, 2, 2, check=True)
    # Master_skill(Mystic_Codes.Chaldea_Combat_Uniform, 1)
    card(1)
